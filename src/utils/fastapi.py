import logging

import httpx
import redis
from fastapi import FastAPI, HTTPException

from src.core import get_settings
from .helpers import generate_user_hash

logger = logging.getLogger("app")

app = FastAPI()
r = redis.Redis(host="redis", port=6379, decode_responses=True)

LOGIN_KEY = "bot:jwt"


async def get_logged_in() -> bool:
    jwt: str = r.get(LOGIN_KEY)  # type: ignore
    if not jwt: return False
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            res = await client.get(f"http://{get_settings().main_backend_host}:8080/api/user/profile", headers={"x-api-secret": get_settings().api_secret, "x-jwt": jwt})
    except Exception:
        logger.error("err_type=get_logged_in", exc_info=True)
        return False
    return res.status_code == 200


@app.get("/status")
async def status():
    return {"logged_in": await get_logged_in()}


@app.post("/login", status_code=204)
async def login():
    if await get_logged_in(): return
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            res = await client.post(f"http://{get_settings().main_backend_host}:8080/api/user/login", headers={"x-api-secret": get_settings().api_secret}, json={"email": "bot@discord.com", "hashToken": generate_user_hash("bot@discord.com")})
    except Exception:
        logger.error("err_type=login ; err_code=504 ; Login request failed", exc_info=True)
        raise HTTPException(status_code=504, detail="Login request failed")

    if res.status_code == 200:
        token = res.json().get("jwt")
        if not token:
            logger.error("err_type=login ; err_code=502 ; Login succeeded but no token was returned")
            raise HTTPException(status_code=502, detail="Login succeeded but no token was returned")
        r.set(LOGIN_KEY, token)
    else:
        logger.error("err_type=login ; err_code=400 ; Login failed")
        raise HTTPException(400, detail=res.text)


def logout():
    r.delete(LOGIN_KEY)
