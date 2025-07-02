import asyncio
from src.utils import consume_rabbitmq
from src.bot.discord import DiscordBotConnector
from src.core import get_settings

async def start_all():
    connector = DiscordBotConnector(command_prefix=get_settings().command_prefix, debug=True)
    connector.start(get_settings().token)

    # Wait until the bot is ready (non-blocking)
    while not connector.bot.is_ready():
        await asyncio.sleep(1)

    print("[MAIN] Bot is ready. Starting RabbitMQ consumer...")
    await consume_rabbitmq(connector)

    # OR: If you want to run more background tasks, do:
    # task = asyncio.create_task(consume_rabbitmq(connector))
    # await task
    
    
if __name__ == "__main__":
    asyncio.run(start_all())
