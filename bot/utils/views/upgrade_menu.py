import discord

from ..imagetools import ImageGen
from .select_menu import RoofSelector, TopSelector, WallSelector
from .shop_create import ShopCreate
import os


class ShopEdit(discord.ui.View):
    def __init__(self, ctx, *, timeout: int = 180):
        self.bot = ctx.bot
        self.ctx = ctx
        super().__init__(timeout=timeout)

    def default(self):
        return {
            "world": [],
            "roof": [],
            "top": [],
            "wall": [],
            "quality": 1,
            "price": 1,
        }

    async def build_embed(self, conf: dict = None):
        if not conf:
            conf = self.conf
        embed = discord.Embed(
            title=f"**~ shop editor ~**",
            color=0x2F3136,
        )
        if self.conf.get("world"):
            img, filename = ImageGen().gen(conf)
            embed.set_image(url=f"attachment://{filename}")
        return embed, img

    @discord.ui.button(label="shop editor", style=discord.ButtonStyle.green)
    async def shop_editor(self, interaction: discord.Interaction, _):
        conf = (await self.bot.db.shop.find_one({"_id": self.ctx.author.id}))["conf"]
        await interaction.response.edit_message(view=ShopCreate(self.ctx, conf=conf))

    @discord.ui.button(label="buy parts", style=discord.ButtonStyle.green)
    async def buy_menu(self, interaction: discord.Interaction, _):
        conf = await self.bot.db.up.find_one({"_id": self.ctx.author.id})
        for i in self.children:
            self.remove_item(i)
        self.add_item(buy_menu_wall(self, conf))
        await interaction.response.edit_message(view=self)


class buy_menu_wall(discord.ui.Select):
    def __init__(self, view, up):
        self._view = view
        options = []
        for i in os.listdir("./assets/shop/wall/"):
            if i.endswith(".png"):
                if i[:-4] not in up["wall"]:
                    options.append(discord.SelectOption(label=i[:-4], value=i[:-4]))
        super().__init__(
            placeholder="Select a roof", max_values=1, min_values=1, options=options
        )

    async def callback(self, interaction: discord.Interaction):
        profile = await self._view.bot.db.economy.find_one(
            {"_id": self._view.ctx.author.id}
        )
        if profile.get("wallet") < 100:
            await interaction.response.edit_message(
                content="You don't have enough money"
            )
            return
        await self._view.bot.db.economy.update_one(
            {"_id": self._view.ctx.author.id}, {"$inc": {"wallet": -100}}
        )
        doc = await self._view.bot.db.up.find_one({"_id": self._view.ctx.author.id})
        doc["wall"].append(self.values[0])
        await self._view.bot.db.up.update_one(
            {"_id": self._view.ctx.author.id}, {"$set": {"wall": doc["wall"]}}
        )
        await interaction.response.edit_message("bought wall")
