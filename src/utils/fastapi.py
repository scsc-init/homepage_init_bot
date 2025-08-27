from fastapi import FastAPI, HTTPException
import redis
import httpx

from src.core import get_settings


app = FastAPI()
r = redis.Redis(host="redis", port=6379, decode_responses=True)

LOGIN_KEY = "bot:jwt"


async def get_logged_in() -> bool:
    async with httpx.AsyncClient() as client:
        jwt = r.get(LOGIN_KEY)
        if not jwt: return False
        res = await client.get(f"http://{get_settings().main_backend_host}:8080/api/user/profile", headers={"x-api-secret": get_settings().api_secret, "x-jwt": jwt})
        if res.status_code != 200: return False
        return True


@app.get("/status")
async def status():
    return {"logged_in": await get_logged_in()}


@app.post("/login", status_code=204)
async def login():
    if await get_logged_in(): return
    async with httpx.AsyncClient() as client:
        res = await client.post(f"http://{get_settings().main_backend_host}:8080/api/user/login", headers={"x-api-secret": get_settings().api_secret}, json={"email": "bot@discord.com"})

        if res.status_code == 200:
            token = res.json().get("jwt")
            r.set(LOGIN_KEY, token)
        else: raise HTTPException(400, detail=res.text)


def logout():
    r.delete(LOGIN_KEY)
