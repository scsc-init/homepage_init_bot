import asyncio
import logging
import pathlib
from types import SimpleNamespace
from typing import Iterable, Optional

import discord
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger("app")


class DiscordBot(commands.Bot):
    def __init__(self, data: dict | None = None, connectors: Optional[Iterable] = None, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.queue = asyncio.Queue()
        self.running_queue_task = False
        self.cc = SimpleNamespace()
        self.connectors = connectors or []

    async def setup_hook(self):
        for path in pathlib.Path("cogs").glob("*.py"):
            await self.load_extension("cogs." + path.stem)

        @app_commands.command(name="enroll", description="Enrolls the user to the discord server")
        @app_commands.describe(student_id="학번(ex. 202500001)")
        async def enroll(interaction: discord.Interaction, student_id: int):
            user = interaction.user
            try:
                for connector in self.connectors:
                    for listener in connector.enroll_event_listeners:
                        res = await listener(connector, student_id, user.id, user.name)
                        await interaction.response.send_message(f"{res}", ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"Error: {e}", ephemeral=True)

        self.tree.add_command(enroll)
        await self.tree.sync()

    async def on_ready(self):
        logger.info(f"info_type=on_ready ; Logged in as {self.user.name}({self.user.id})")
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
