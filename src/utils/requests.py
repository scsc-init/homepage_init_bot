import httpx

from src.bot.discord import SCSCBotConnector
from src.core import get_settings


async def enroll_user(connector: SCSCBotConnector, student_id: int, user_id: int, user_name: str):
    return f'{user_id}, {user_name}, {student_id}'

            
            
