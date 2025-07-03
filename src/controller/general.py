from src.bot.discord import SCSCBotConnector

async def create_invite(connector: SCSCBotConnector, body: dict):
    invite = connector.create_invite()
    return {"invite_url": str(invite)}

async def send_message_by_id(connector: SCSCBotConnector, body: dict):
    connector.send_message(body['id'], body['content'])
    
async def send_message_by_name(connector: SCSCBotConnector, body: dict):
    connector.send_message(body['name'], body['content'])
    
async def get_id_from_name(connector: SCSCBotConnector, body: dict):
    channel = connector.get_channel(body['name'])
    if channel: return channel.id
    