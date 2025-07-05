import discord

from src.bot.discord import SCSCBotConnector

async def create_invite(connector: SCSCBotConnector, body: dict):
    invite = connector.create_invite()
    return {"invite_url": str(invite)}

async def send_message_by_id(connector: SCSCBotConnector, body: dict):
    if body['embed']: 
        embed = discord.Embed(title=body['embed'].get("title"), description=body['embed'].get("description"), color=discord.Color(body['embed'].get("color")))
        for field in body['embed'].get("fields", []):
            embed.add_field(name=field.get("name"), value=field.get("value"),inline=field.get("inline", True))
        connector.send_message(body['channel_id'], body['content'], embed)
        return
    connector.send_message(body['channel_id'], body['content'])
    
async def send_message_by_name(connector: SCSCBotConnector, body: dict):
    if body['embed']: 
        embed = discord.Embed(title=body['embed'].get("title"), description=body['embed'].get("description"), color=discord.Color(body['embed'].get("color")))
        for field in body['embed'].get("fields", []):
            embed.add_field(name=field.get("name"), value=field.get("value"),inline=field.get("inline", True))
        connector.send_message(body['channel_name'], body['content'], embed)
        return
    connector.send_message(body['channel_name'], body['content'])
    
async def get_id_from_name(connector: SCSCBotConnector, body: dict):
    channel = connector.get_channel(body['channel_name'])
    if channel: return {"channel_id": channel.id}
    