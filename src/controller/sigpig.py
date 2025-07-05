from src.bot.discord import SCSCBotConnector

async def update_sig_category(connector: SCSCBotConnector, body: dict):
    connector.update_sig_category(body['category_name'], create=True)

async def update_sig_archive_category(connector: SCSCBotConnector, body: dict):
    connector.update_sig_archive_category(body['category_name'], create=True)

async def get_category_from_name(connector: SCSCBotConnector, body: dict):
    category = connector.get_category(body['category_name'])
    if category: return {'category_id': category.id}
    
async def create_channel(connector: SCSCBotConnector, body: dict):
    connector.create_text_channel(body['channel_name'], body['category_id'])
    
async def move_channel(connector: SCSCBotConnector, body: dict):
    connector.edit_text_channel(body['channel_id'], name=body['new_channel_name'], category_identifier=body['category_to_id'])
    