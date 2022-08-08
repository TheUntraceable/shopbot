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
            await self.bot.db.levelling.insert_one({
                "user_id": ctx.author.id,
                "xp": 1
            })
        document = await self.bot.db.levelling.find_one({
            "user_id": ctx.author.id
        })
        await ctx.reply(f"{ctx.author.mention} you have {document['xp']} xp, which makes you level {self.get_level(document['xp'])}!")

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.guild)
    async def attack(self, ctx):
        document = await self.bot.db.levelling.find_one({"user_id": ctx.author.id}) or {"xp": 1}

        damage = randint(0,5*self.get_level(document['xp']))

        results = await self.bot.db.damage_contribution.update_one({
            "guild_id": ctx.guild.id
        }, {"$inc": {"damage": damage}}, upsert=False)

        await ctx.reply(f"You have dealt {damage}!")

        if not document.get("user_id"):
            await self.bot.db.levelling.insert_one({
                "user_id": ctx.author.id,
                "xp": 1
            })
        if not results.modified_count:
            await self.bot.db.damage_contribution.insert_one({
                "guild_id": ctx.guild.id,
                "damage": damage
            })

    @commands.command()
    async def damage(self, ctx):
        document = await self.bot.db.damage_contribution.find_one({"guild_id": ctx.guild.id})
        if document is None:
            await self.bot.db.damage_contribution.insert_one({
                "guild_id": ctx.guild.id,
                "damage": 0
            })
        document = await self.bot.db.damage_contribution.find_one({"guild_id": ctx.guild.id})
        guilds = []
        async for guild in self.bot.db.damage_contribution.find():
            guilds.append(guild)
        guilds.sort("xp", -1)        
        await ctx.reply(f"This server has dealt {document['damage']} damage! It is rank number {guilds.index(document)} on the leaderboard.")

async def setup(bot):
    await bot.add_cog(LevellingTheme(bot))
