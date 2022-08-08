from typing import TYPE_CHECKING
import discord
from discord.ext import commands
import time
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
    
    def defaults(self,user):
        return {
            "_id":user.id,
            "name": f"{user.name}'s shop",
            "description": f"{user.name} hasnt bothered to enter a description yet",
            "items": [],
            "level": 0,
            "price": 1, 
            "sales": 0,
            "stock": 0,
            "made_at":time.time(),
            "conf":{}
        }

    @shop.command(name="new", aliases=["create"])
    async def shop_new(self, ctx):
        """Create a new shop."""
        if self.bot.db.shop.count_documents({ '_id': ctx.author.id }, limit = 1):
            await ctx.reply("You already have a shop.")
            return
        embed = discord.Embed(
            title=f"**~ welcome to the start of your journey ~**", color=0x2F3136
        )
        msg = await ctx.reply("getting everything ready for you...", embed=embed)
        await self.bot.db.shop.insert_one(self.defaults(ctx.author))
        setattr(ctx, "bot_msg", msg)
        await msg.edit(content="", embed=embed, view=ShopCreate(ctx))


async def setup(bot):
    await bot.add_cog(Shops(bot))
