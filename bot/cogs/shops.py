from typing import TYPE_CHECKING
import discord
from discord.ext import commands
import time
from ..utils.views import ShopCreate
from ..utils.imagetools.image_gen import ImageGen

if TYPE_CHECKING:
    from ..bot import Bot


class Shops(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.group(name="shop", invoke_without_command=True)
    async def shop(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid shop command passed.")

    def defaults(self, user):
        return {
            "_id": user.id,
            "name": f"{user.name}'s shop",
            "description": f"{user.name} hasnt bothered to enter a description yet",
            "items": [],
            "level": 0,
            "price": 1,
            "sales": 0,
            "stock": 0,
            "made_at": time.time(),
            "conf": {},
        }

    @shop.command(name="new", aliases=["create"])
    async def shop_new(self, ctx):
        """Create a new shop."""
        if not await self.bot.db.shop.find_one({"_id": ctx.author.id}):
            await self.bot.db.shop.insert_one(self.defaults(ctx.author))
        if (await self.bot.db.shop.find_one({"_id": ctx.author.id}))["conf"].get(
            "world"
        ):
            await ctx.reply("You already have a shop.")
            return
        embed = discord.Embed(
            title=f"**~ welcome to the start of your journey ~**", color=0x2F3136
        )
        msg = await ctx.reply("getting everything ready for you...", embed=embed)

        setattr(ctx, "bot_msg", msg)
        await msg.edit(content="", embed=embed, view=ShopCreate(ctx))

    @shop.command(name="stats", aliases=["stat"])
    async def shop_stats(self, ctx):
        """View your shop.and stats"""
        m = await ctx.reply("fetching image")
        profile = await self.bot.db.shop.find_one({"_id": ctx.author.id})
        embed = discord.Embed(
            title=f"**your shop**",
            color=0x2F3136,
            description=f"```\n{profile['description']}\n```\n```yaml\n{str(profile['name'])}\n```",
        )
        img, p = ImageGen().gen(profile["conf"])
        items = "\n> ".join(profile["items"]) or "None"
        embed.add_field(name="`items`", value=f"{items}", inline=False)
        embed.add_field(name="`level`", value=f"> {profile['level']}", inline=False)
        embed.add_field(name="`sales`", value=f"> {profile['sales']}", inline=True)
        embed.add_field(name="`stock`", value=f"> {profile['stock']}", inline=False)
        embed.set_image(url="attachment://" + p)
        await m.edit(content="", attachments=[img], embed=embed)


async def setup(bot):
    await bot.add_cog(Shops(bot))
