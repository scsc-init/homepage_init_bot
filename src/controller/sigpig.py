from src.bot.discord import SCSCBotConnector

async def update_sig_category(connector: SCSCBotConnector, body: dict):
    connector.update_sig_category(body['category_name'], create=False)

async def update_sig_archive_category(connector: SCSCBotConnector, body: dict):
    connector.update_sig_archive_category(body['category_name'], create=True)

async def update_pig_category(connector: SCSCBotConnector, body: dict):
    connector.update_pig_category(body['category_name'], create=False)

async def update_pig_archive_category(connector: SCSCBotConnector, body: dict):
    connector.update_pig_archive_category(body['category_name'], create=True)

async def get_category_from_name(connector: SCSCBotConnector, body: dict):
    category = connector.get_category(body['category_name'])
    if category: return {'category_id': category.id}
    
async def create_channel(connector: SCSCBotConnector, body: dict):
    connector.create_text_channel(body['channel_name'], body['category_id'], body.get('topic', None))
    
async def edit_channel(connector: SCSCBotConnector, body: dict):
    params = {}
    if 'new_channel_name' in body:
        params['name'] = body['new_channel_name']
    if 'category_id_to_move' in body:
        params['category_identifier'] = body['category_id_to_move']
    if 'new_topic' in body:
        params['topic'] = body['new_topic']
    connector.edit_text_channel(body['channel_id'], **params)
    
async def update_data(connector: SCSCBotConnector, body: dict):
    connector.set_data(body['data'])
