from src.bot.discord import DiscordBotConnector

async def create_invite(connector: DiscordBotConnector):
    invite = connector.create_invite()
    return {"invite_url": str(invite)}

