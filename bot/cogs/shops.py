import discord
from discord.ext import commands

from ..utils.components import Item, Shop
from ..utils.views import ShopCreate


class Shops(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="shop", invoke_without_command=True)
    async def shop(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid shop command passed.")

    @shop.command(name="new", aliases=["create"])
    async def shop_new(self, ctx):
        """Create a new shop."""
        embed = discord.Embed(
            title=f"**~ welcome to the start of your journey ~**", color=0x2F3136
        )
        msg = await ctx.reply("getting everything ready for you...", embed=embed)
        await msg.edit(content="", embed=embed, view=ShopCreate())


async def setup(bot):
    await bot.add_cog(Shops(bot))
