import httpx
import redis

from src.bot.discord import SCSCBotConnector
from src.core import get_settings

r = redis.Redis(host="redis", port=6379, decode_responses=True)
LOGIN_KEY = "bot:jwt"


async def enroll_user(
    connector: SCSCBotConnector,
    student_id: int,
    discord_user_id: int,
    discord_user_name: str,
):
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"http://{get_settings().main_backend_host}:8080/api/users",
            headers={"x-api-secret": get_settings().api_secret},
            params={"student_id": student_id},
        )
        if res.status_code != 200 or not res.json():
            raise ValueError(
                "Invalid input from user, please check your student id input"
            )
        user_id = res.json()[0].get("id")
        user_role = res.json()[0].get("role")
        user_discord_id = res.json()[0].get("discord_id")
        if user_discord_id:
            raise Exception(f"User with student id {student_id} already enrolled")
        if r.get(LOGIN_KEY) is None:
            raise Exception("Bot is not logged in")
        res = await client.post(
            f"http://{get_settings().main_backend_host}:8080/api/executive/user/{user_id}",
            headers={
                "x-api-secret": get_settings().api_secret,
                "x-jwt": str(r.get(LOGIN_KEY)),
            },
            json={"discord_id": discord_user_id, "discord_name": discord_user_name},
        )
        if res.status_code != 204:
            raise Exception(
                f"User discord id enroll failed with status {res.status_code}:{res.json()}"
            )
        res = await client.get(
            f"http://{get_settings().main_backend_host}:8080/api/role_names",
            headers={"x-api-secret": get_settings().api_secret},
        )
        user_role = res.json().get("role_names").get(str(user_role))
        try:
            if connector.get_role(user_role):
                await connector.get_member(discord_user_id).add_roles(
                    connector.get_role(user_role)
                )
                return "Success!"
            else:
                raise Exception(f"Role {user_role} does not exist")
        except Exception as e:
            raise Exception(f"User discord id enroll failed with exception: {e}")
