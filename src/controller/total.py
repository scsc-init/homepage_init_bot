from src.bot.discord import SCSCBotConnector

async def create_sig(connector: SCSCBotConnector, body: dict):
    connector.create_sig(body['sig_name'], body['user_id_list'], body.get('sig_description', None))
    
async def archive_sig(connector: SCSCBotConnector, body: dict):
    connector.archive_sig(body['sig_name'], previous_semester=body['previous_semester'])
    
async def create_pig(connector: SCSCBotConnector, body: dict):
    connector.create_pig(body['pig_name'], body['user_id_list'], body.get('pig_description', None))
    
async def archive_pig(connector: SCSCBotConnector, body: dict):
    connector.archive_pig(body['pig_name'], previous_semester=body['previous_semester'])
