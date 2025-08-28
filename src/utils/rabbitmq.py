import asyncio
import json
import logging

import aio_pika
from aiormq.exceptions import AMQPConnectionError

from src.bot.discord import SCSCBotConnector
from src.core import get_settings
from src.utils.dispatcher import dispatch

logger = logging.getLogger("app")


async def consume_rabbitmq(connector: SCSCBotConnector):
    rabbitmq_hostname = get_settings().rabbitmq_host
    connection = None
    while connection is None:
        try:
            connection = await aio_pika.connect_robust(f"amqp://guest:guest@{rabbitmq_hostname}/")
        except AMQPConnectionError as e:
            logger.error(f"err_type=consume_rabbitmq ; [RabbitMQ] Connection failed, retrying in 2 seconds... ({e})")
            await asyncio.sleep(2)
    channel = await connection.channel()
    queue = await channel.declare_queue(get_settings().discord_receive_queue, durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                payload = json.loads(message.body)
                action_code = payload.get("action_code")
                body = payload.get("body", {})
                reply_to = payload.get("reply_to")
                correlation_id = payload.get("correlation_id")

                try:
                    handler = dispatch(action_code)
                    result = await handler(connector, body)
                    if reply_to:
                        logger.info(f"info_type=consume_rabbitmq ; {result}")
                        await channel.default_exchange.publish(
                            aio_pika.Message(
                                body=json.dumps({"correlation_id": correlation_id, "result": result}).encode(),
                                correlation_id=correlation_id
                            ),
                            routing_key=reply_to
                        )
                except Exception as e: logger.error(f"err_type=consume_rabbitmq ; Error: {e}")
