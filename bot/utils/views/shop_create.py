import discord

from ..imagetools import ImageGen
from .select_menu import RoofSelector, TopSelector, WallSelector


class ShopCreate(discord.ui.View):
    def __init__(self,ctx, *, timeout: int = 180):
        self.ctx = ctx
        super().__init__(timeout=timeout)
        self.conf = {}
    
    async def top_phase(self):
        for child in self.children:
            self.remove_item(child)
        self.add_item(TopSelector(self,self.conf))
        await self.ctx.bot_msg.edit(view=self)
            
    async def roof_phase(self):
        for child in self.children:
            self.remove_item(child)
        self.add_item(RoofSelector(self,self.conf))
        await self.ctx.bot_msg.edit(view=self)
    
    async def wall_phase(self):
        for child in self.children:
            self.remove_item(child)
        self.add_item(WallSelector(self,self.conf))
        await self.ctx.bot_msg.edit(view=self)

    async def build_embed(self,conf:dict=None):
        if not conf:
            conf = self.conf
        embed = discord.Embed(
            title=f"**~ welcome to the start of your journey ~**", color=0x2F3136
        )
        img,filename = ImageGen().gen(conf)
        if self.conf.get("world"):
            embed.set_image(url=f"attachment://{filename}")
        return embed,[img]

    @discord.ui.button(label="farm", style=discord.ButtonStyle.green)
    async def farmside(self, interaction: discord.Interaction, _):
        self.conf["world"] = "farm"
        # await interaction.response.send_message("farmside selected.",ephemeral=True)
        embed,img = await self.build_embed()
        await interaction.response.edit_message(attachments=img,embed=embed)
        await self.wall_phase()

    @discord.ui.button(label="city", style=discord.ButtonStyle.gray)
    async def metropolis(self, interaction: discord.Interaction, _):
        self.conf["world"] = "city"
        # await interaction.response.send_message("metropolis selected.",ephemeral=True)
        embed,img = await self.build_embed()
        await interaction.response.edit_message(attachments=img,embed=embed)
        await self.wall_phase()

    @discord.ui.button(label="nether", style=discord.ButtonStyle.red)
    async def underworld(self, interaction: discord.Interaction, _):
        self.conf["world"] = "nether"
        # await interaction.response.send_message("underworld selected.",ephemeral=True)
        embed,img = await self.build_embed()
        await interaction.response.edit_message(attachments=img,embed=embed)
        await self.wall_phase()
