import json
import logging
import os
import time

import discord
from discord.ext import commands
from rich.console import Console
from rich.logging import RichHandler
from .utils.util_classes.db import Database


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        # init logging
        self.set_logging()

        # init conf
        with open("./config.json") as f:
            config = json.load(f)
        self.token = config["token"]

        # init database
        self.db = Database()

        # store start time
        self.start_time = time.time()

        # create commands.Bot
        super().__init__(
            command_prefix=";",
            intents=discord.Intents.all(),
            *args,
            **kwargs,
            owner_ids=[482139697796349953, 507969622876618754, 903667860499484742],
        )

    def set_logging(self):
        FORMAT = "%(message)s"
        self.console = Console()
        logging.basicConfig(
            level=logging.INFO,
            format=FORMAT,
            datefmt="[%X]",
            handlers=[RichHandler(rich_tracebacks=True, console=self.console)],
        )
        self.log = logging.getLogger("rich")
        self.log.info("Logging set up.")

    async def on_ready(self):
        self.log.info(f"Logged in as {self.user.name}")
        self.log.info(f"Connected to {len(self.guilds)} servers")
        self.log.info(f"Connected to {len(self.users)} users")
        self.log.info(f"Bot uptime: {time.time() - self.start_time} seconds")
        await self.load_cogs()

    async def load_cogs(self):
        for filename in os.listdir("./bot/cogs"):
            if filename.endswith(".py"):
                self.log.info(f"Loading cogs: {filename[:-3]}")
                await self.load_extension(f"bot.cogs.{filename[:-3]}")

    async def unload_cogs(self):
        for cog in self.cogs:
            self.log.info(f"Unloading cogs: {cog}")
            await self.unload_extension(f"bot.cogs.{cog}")

    def run(self):
        self.log.info("Starting bot...")
        super().run(self.token)
