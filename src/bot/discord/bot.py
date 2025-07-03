import discord
from discord.ext import commands
import pathlib
import json
from types import SimpleNamespace
from typing import Optional, Iterable

import asyncio

class SCSCBot(commands.Bot):
    def __init__(self, data: dict = None, connectors: Optional[Iterable] = None, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.queue = asyncio.Queue()
        self.running_queue_task = False
        self.cc = SimpleNamespace()
        self.connectors = connectors or []

    async def setup_hook(self):
        for path in pathlib.Path("cogs").glob("*.py"):
            await self.load_extension("cogs." + path.stem)
        await self.tree.sync()

    async def on_ready(self):
        print(f"Logged in as {self.user.name}({self.user.id})")
        for connector in self.connectors:
            connector.bot_on_ready()

    # async def runQueue(self):
    #     if self.running_queue_task:
    #         return
    #     self.running_queue_task = True
    #     try:
    #         while not self.queue.empty():
    #             coro = await self.queue.get()
    #             try:
    #                 await coro
    #             except Exception as e:
    #                 print(f"[Queue Error] {e}")
    #     finally:
    #         self.running_queue_task = False
    #
    # def runQueueNowait(self):
    #     if not self.running_queue_task and self.loop.is_running():
    #         asyncio.run_coroutine_threadsafe(self.runQueue(), self.loop)

    def run(self, token: str, **kwargs):
        return super().run(token=token, **kwargs)

    async def start(self, token: str, *, reconnect: bool = True) -> None:
        return await super().start(token, reconnect=reconnect)