import asyncio
from threading import Thread
import uvicorn

from src.utils import consume_rabbitmq
from src.bot.discord import SCSCBotConnector
from src.core import get_settings
from src.utils import fastapi_app, enroll_user, login
            

def run_fastapi(): uvicorn.run(fastapi_app, host='0.0.0.0', port=8081)

async def start_all():
    fastapi_thread = Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    
    connector = SCSCBotConnector(command_prefix=get_settings().command_prefix, debug=True)
    try:
        await login()
    except Exception as e:
        print(f"Login failed with exception: {e}")
    connector.enroll_event_listeners.append(enroll_user)
    connector.start(get_settings().token)

    while not connector.bot.is_ready():
        await asyncio.sleep(1)

    await consume_rabbitmq(connector)

    

    
if __name__ == "__main__":
    asyncio.run(start_all())
