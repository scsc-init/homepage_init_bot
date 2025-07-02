import json
import aio_pika


from src.utils.dispatcher import dispatch
from src.bot.discord import DiscordBotConnector
from src.core import get_settings


async def consume_rabbitmq(connector: DiscordBotConnector):
    rabbitmq_hostname = get_settings().rabbitmq_host
    connection = await aio_pika.connect_robust(f"amqp://guest:guest@{rabbitmq_hostname}/")
    channel = await connection.channel()
    queue = await channel.declare_queue("bot_queue", durable=True)

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
                        print(result)
                        await channel.default_exchange.publish(
                            aio_pika.Message(
                                body=json.dumps({"correlation_id": correlation_id, "result": result}).encode(),
                                correlation_id=correlation_id
                            ),
                            routing_key=reply_to
                        )
                except Exception as e: print(f"Error: {e}")
