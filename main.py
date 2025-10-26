import asyncio
import logging.config
from threading import Thread

import uvicorn

from src.bot.discord import SCSCBotConnector
from src.core import get_settings
from src.middleware import (
    HTTPLoggerMiddleware,
)
from src.util import (
    LOGGING_CONFIG,
    consume_rabbitmq,
    enroll_user,
    fastapi_app,
    login,
    logout,
)

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("app")


def run_fastapi():
    fastapi_app.add_middleware(HTTPLoggerMiddleware)
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8081)


async def start_all():
    fastapi_thread = Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()

    connector = SCSCBotConnector(
        command_prefix=get_settings().command_prefix, debug=True
    )
    logout()
    logger.info("info_type=start_all ; Bot logged out from backend")
    try:
        await login()
    except Exception:
        logger.error("err_type=start_all ; Login failed with exception", exc_info=True)
    connector.enroll_event_listeners.append(enroll_user)
    connector.start(get_settings().token)

    while not connector.bot.is_ready():
        await asyncio.sleep(1)

    await consume_rabbitmq(connector)


if __name__ == "__main__":
    asyncio.run(start_all())
