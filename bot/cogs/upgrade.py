from discord.ext import commands

from ..utils.views.upgrade_menu import ShopEdit


class Upgrade(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="upgrade", aliases=["up"])
    async def upgrade(self, ctx):
        msg = await ctx.reply("getting everything ready for you...")
        setattr(ctx, "bot_msg", msg)
        await msg.edit(content="", view=ShopEdit(ctx))


async def setup(bot):
    await bot.add_cog(Upgrade(bot))
