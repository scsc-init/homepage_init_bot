from fastapi import FastAPI, HTTPException
import redis
import httpx

from src.core import get_settings


app = FastAPI()
r = redis.Redis(host="redis", port=6379, decode_responses=True)

LOGIN_KEY = "bot:jwt"

@app.get("/status")
async def status():
    async with httpx.AsyncClient() as client:
        res = await client.get(f"http://{get_settings().main_backend_host}:8080/api/user/profile", headers={"x-api-secret": get_settings().api_secret})
        if res.status_code != 200: return {"logged_in": False}
        else: return {"logged_in": True}
            

@app.post("/login", status_code=201)
async def login():
    async with httpx.AsyncClient() as client:
        res = await client.post(f"http://{get_settings().main_backend_host}:8080/api/user/login", headers={"x-api-secret": get_settings().api_secret}, json={"email": "bot@discord.com"})

        if res.status_code == 200:
            token = res.json().get("jwt")
            r.set(LOGIN_KEY, token, ex=3600*24*30)
        else:
            raise HTTPException(400, detail=res.text)
