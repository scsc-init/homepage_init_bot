from src.bot.discord import DiscordBotConnector

async def create_sig(connector: DiscordBotConnector, body: dict):
    connector.create_sig(body['sig_name'], body['id_list'])
    
async def archive_sig(connector: DiscordBotConnector, body: dict):
    connector.archive_sig(body['name'])
    