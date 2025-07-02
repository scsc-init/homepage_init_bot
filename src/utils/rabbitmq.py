import json
import aio_pika


from src.utils.dispatcher import dispatch
from src.bot.discord import DiscordBotConnector


async def consume_rabbitmq(connector: DiscordBotConnector):
    print("[BOT] Connecting to RabbitMQ...")
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    channel = await connection.channel()
    print("[BOT] Declaring bot_queue...")
    queue = await channel.declare_queue("bot_queue", durable=True)
    print("[BOT] Waiting for messages on bot_queue...")

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
                    result = await handler(connector)
                    if reply_to:
                        print(result)
                        await channel.default_exchange.publish(
                            aio_pika.Message(
                                body=json.dumps({"correlation_id": correlation_id, "result": result}).encode(),
                                correlation_id=correlation_id
                            ),
                            routing_key=reply_to
                        )
                except Exception as e:
                    print(f"Error handling message: {e}")
