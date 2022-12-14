import discord

from ..imagetools import ImageGen
from .select_menu import RoofSelector, TopSelector, WallSelector


class ShopCreate(discord.ui.View):
    def __init__(self, ctx, *, timeout: int = 180, conf: dict = None):
        self.ctx = ctx
        self.bot = ctx.bot
        super().__init__(timeout=timeout)
        self.conf = conf

    def default_up(self, id):
        return {
            "_id": int(id),
            "world": ["farm"],
            "roof": ["farm"],
            "top": ["farm"],
            "wall": ["farm"],
            "quality": 1,
            "price": 1,
        }

    def default_prof(self, _id):
        return {
            "_id": _id,
            "wallet": 0,
            "bank": 0,
            "max_bank": 0,
            "daily_streak": 0,
        }

    async def update_conf(self):
        prof = await self.bot.economy.up.find_one({"_id": self.ctx.author.id})
        doc = await self.bot.db.up.find_one({"_id": self.ctx.author.id})
        if not prof:
            await self.bot.economy.up.insert_one(self.default_prof(self.ctx.author.id))
        if not doc:
            await self.bot.db.up.insert_one(self.default_up(self.ctx.author.id))
            doc = await self.bot.db.up.find_one({"_id": self.ctx.author.id})
        self.up = doc

    async def save(self):
        for child in self.children:
            self.remove_item(child)
        await self.ctx.bot.db.shop.update_one(
            {"_id": self.ctx.author.id}, {"$set": {"conf": self.conf}}
        )
        await self.ctx.bot_msg.edit(view=self)

    async def top_phase(self):
        for child in self.children:
            self.remove_item(child)
        self.add_item(TopSelector(self, self.conf, self.up))
        await self.ctx.bot_msg.edit(view=self)

    async def roof_phase(self):
        for child in self.children:
            self.remove_item(child)
        self.add_item(RoofSelector(self, self.conf, self.up))
        await self.ctx.bot_msg.edit(view=self)

    async def wall_phase(self):
        for child in self.children:
            self.remove_item(child)
        self.add_item(WallSelector(self, self.conf, self.up))
        await self.ctx.bot_msg.edit(view=self)

    async def build_embed(self, conf: dict = None):
        if not conf:
            conf = self.conf
        embed = discord.Embed(
            title=f"**~ shop editor ~**",
            color=0x2F3136,
        )
        img, filename = ImageGen().gen(conf)
        if self.conf.get("world"):
            embed.set_image(url=f"attachment://{filename}")
        return embed, img

    @discord.ui.button(label="farm", style=discord.ButtonStyle.green)
    async def farmside(self, interaction: discord.Interaction, _):
        await self.update_conf()
        self.conf["world"] = "farm"
        # await interaction.response.send_message("farmside selected.",ephemeral=True)
        embed, img = await self.build_embed()
        await interaction.response.edit_message(attachments=[img], embed=embed)
        await self.wall_phase()

    @discord.ui.button(label="city", style=discord.ButtonStyle.gray)
    async def metropolis(self, interaction: discord.Interaction, _):
        await self.update_conf()
        self.conf["world"] = "city"
        # await interaction.response.send_message("metropolis selected.",ephemeral=True)
        embed, img = await self.build_embed()
        await interaction.response.edit_message(attachments=[img], embed=embed)
        await self.wall_phase()

    @discord.ui.button(label="nether", style=discord.ButtonStyle.red)
    async def underworld(self, interaction: discord.Interaction, _):
        await self.update_conf()
        self.conf["world"] = "nether"
        # await interaction.response.send_message("underworld selected.",ephemeral=True)
        embed, img = await self.build_embed()
        await interaction.response.edit_message(attachments=[img], embed=embed)
        await self.wall_phase()
