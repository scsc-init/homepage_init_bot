from src.bot.discord import SCSCBotConnector

async def give_role_to_id(connector: SCSCBotConnector, body: dict):
    role = connector.get_role(body['role_name'])
    if role: connector.add_role(body['user_id'], role)
    
async def remove_role_from_id(connector: SCSCBotConnector, body: dict):
    role = connector.get_role(body['role_name'])
    if role: connector.remove_role(body['user_id'], role)
    
async def get_ids_from_name(connector: SCSCBotConnector, body: dict):
    return {"id_list": [member.id for member in connector.get_members(body['name'])]}

async def create_role_with_ids(connector: SCSCBotConnector, body: dict):
    connector.create_role(body['role_name', body['id_list']])
    