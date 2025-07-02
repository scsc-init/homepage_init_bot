import asyncio
from src.utils import consume_rabbitmq
from src.bot.discord import DiscordBotConnector
from src.core import get_settings

async def start_all():
    connector = DiscordBotConnector(command_prefix=get_settings().command_prefix, debug=True)
    connector.start(get_settings().token)

    while not connector.bot.is_ready():
        await asyncio.sleep(1)

    await consume_rabbitmq(connector)

    
    
if __name__ == "__main__":
    asyncio.run(start_all())
