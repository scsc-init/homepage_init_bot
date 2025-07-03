from src.bot.discord import DiscordBotConnector

async def create_category(connector: DiscordBotConnector, body: dict):
    connector.create_category(body['name'])

async def edit_category(connector: DiscordBotConnector, body: dict):
    pass

async def get_category_from_name(connector: DiscordBotConnector, body: dict):
    category = connector.get_category(body['name'])
    if category: return {'id': category.id}
    
async def create_channel(connector: DiscordBotConnector, body: dict):
    connector.create_text_channel(body['channel_name'], body['category_id'])
    
async def move_channel(connector: DiscordBotConnector, body: dict):
    connector.edit_text_channel(body['channel_id'], name=body['new_channel_name'], category_identifier=body['category_to_id'])