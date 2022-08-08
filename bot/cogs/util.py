import json
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from ..utils.imagetools import ImageGen

if TYPE_CHECKING:
    from ..bot import Bot


class Util(commands.Cog):
    def __init__(self, bot):
        self.bot: "Bot" = bot

    @commands.command()
    async def del_rec(self, ctx, col, id):
        await self.bot.db.__getattribute__(col).delete_one({"_id": int(id)})
        await ctx.send(f"{id} has been deleted")

    @commands.command()
    async def show_rec(self, ctx, col, id):
        e = await self.bot.db.__getattribute__(col).find_one({"_id": int(id)})
        await ctx.send(e)

    @commands.command()
    async def gen_image(self, ctx, *, conf: str):
        await ctx.send(file=ImageGen().gen(json.loads(conf)))

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def unloadcog(self, ctx, extension):
        self.bot.log.info(f"Unloading cog {extension}")
        await self.bot.unload_extension(f"bot.commands.{extension}")
        await ctx.send(f"Unloaded {extension}")

    @commands.command()
    async def loadcog(self, ctx, extension):
        self.bot.log.info(f"Loading cog {extension}")
        await self.bot.load_extension(f"bot.commands.{extension}")
        await ctx.send(f"Reloaded {extension}")

    @commands.command()
    async def reloadcog(self, ctx, extension):
        if extension == "all":
            await self.bot.unload_cogs()
            await self.bot.load_cogs()
        else:
            self.bot.log.info(f"Unloading cog {extension}")
            await self.bot.unload_extension(f"bot.commands.{extension}")
            self.bot.log.info(f"Loading cog {extension}")
            await self.bot.load_extension(f"bot.commands.{extension}")
            await ctx.send(f"Reloaded {extension}")

    @commands.command()
    async def cogs(self, ctx):
        out = ""
        out += "\n".join(self.bot.cogs)
        await ctx.send(f"```py\n{out}\n```")


async def setup(bot):
    await bot.add_cog(Util(bot))
