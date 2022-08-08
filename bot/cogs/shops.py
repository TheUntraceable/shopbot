from typing import TYPE_CHECKING
import discord
from discord.ext import commands

from ..utils.views import ShopCreate

if TYPE_CHECKING:
    from ..bot import Bot


class Shops(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.group(name="shop", invoke_without_command=True)
    async def shop(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid shop command passed.")

    @shop.command(name="new", aliases=["create"])
    async def shop_new(self, ctx):
        """Create a new shop."""
        if self.bot.db.shop.get_shops(ctx.author.id):
            await ctx.send("You already have a shop.")
            return
        embed = discord.Embed(
            title=f"**~ welcome to the start of your journey ~**", color=0x2F3136
        )
        msg = await ctx.reply("getting everything ready for you...", embed=embed)
        setattr(ctx, "bot_msg", msg)
        setattr(ctx, "me", self.bot)
        await msg.edit(content="", embed=embed, view=ShopCreate(ctx))


async def setup(bot):
    await bot.add_cog(Shops(bot))
