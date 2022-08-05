from discord.ext import commands
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import Bot


class LevellingTheme(
    commands.Cog
):  # This is the cog which will handle the "Levelling" theme.
    def __init__(self, bot: Bot):
        self.bot = bot
