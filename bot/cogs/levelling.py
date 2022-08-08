from asyncio import sleep
from random import randint
from discord.ext import commands
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import Bot


class LevellingTheme(
    commands.Cog
):  # This is the cog which will handle the "Levelling" theme.
    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.levelling_cooldowns = set()
        self.BOSS_HEALTH = 1e9 # 1 Billion? idk

    @commands.Cog.listener()
    async def on_message(self, message):

        if (
            message.author.id in self.levelling_cooldowns
            or message.author.bot
            or message.guild is None
        ):
            return

        self.levelling_cooldowns.add(message.author.id)
        document = await self.bot.db.levelling.find_one({
            "user_id": message.author.id
        })
        await self.bot.db.levelling.update_one(
            {"user_id": message.author.id},
            {"$inc": {"xp": int(1 * randint(0, 5.909841093821093821098))}},
        )
        await sleep(15)
        self.levelling_cooldowns.remove(message.author.id)

    def get_level(self,xp):
        level = 0
        while xp > ((50*(level**2)) + (50*level)):
            level += 1
        return level

    @commands.command(name="level", aliases=["lvl"])
    async def level(self, ctx):
        document = await self.bot.db.levelling.find_one({"user_id": ctx.author.id})
        if document is None:
            await self.bot.db.levelling.insert_one({"user_id": ctx.author.id, "xp": 0})
            document = await self.bot.db.levelling.find_one({"user_id": ctx.author.id})
        await ctx.send(f"{ctx.author.mention} you have {document['xp']} xp!")


async def setup(bot):
    await bot.add_cog(LevellingTheme(bot))
