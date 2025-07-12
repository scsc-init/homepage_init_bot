from src.bot.discord import SCSCBotConnector

async def create_sig(connector: SCSCBotConnector, body: dict):
    connector.create_sig(body['sig_name'], body['user_id_list'])
    
async def archive_sig(connector: SCSCBotConnector, body: dict):
    connector.archive_sig(body['sig_name'])
    
async def create_pig(connector: SCSCBotConnector, body: dict):
    connector.create_pig(body['pig_name'], body['user_id_list'])
    
async def archive_pig(connector: SCSCBotConnector, body: dict):
    connector.archive_pig(body['pig_name'])
