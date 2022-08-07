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

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.id in self.levelling_cooldowns or message.author.bot or message.guild is None:
            return

        self.levelling_cooldowns.add(message.author.id)
        await self.bot.db.levelling
        self.levelling_cooldowns.remove(message.author.id)

async def setup(bot):
    await bot.add_cog(LevellingTheme(bot))