import discord

from .select_menu import WallSelector


class ShopCreate(discord.ui.View):
    def __init__(self, ctx, *, timeout: int = 180):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.conf = {}

    async def interaction_check(self, interaction):
        return interaction.user.id == self.ctx.author.id

    async def build_embed(
        self, phase_str: str = "welcome to the start of your journey"
    ):
        assets = {
            "farmside": "https://media.discordapp.net/attachments/1004758257707008050/1004758318855749732/farmside.png",
            "metropolis": "https://media.discordapp.net/attachments/1004758257707008050/1004758318209835008/metropolis.png",
            "underworld": "https://media.discordapp.net/attachments/1004758257707008050/1004758318553763870/underworld.png",
        }
        embed = discord.Embed(title=f"**~ {phase_str} ~**", color=0x2F3136)
        if self.conf.get("world"):
            embed.set_image(url=assets.get(self.conf["world"]))
        return embed

    async def wall_phase(self):
        for button in self.children:
            if button.label in ["farmside", "metropolis", "underworld"]:
                self.remove_item(button)
        self.add_item(WallSelector(self.conf))
        await self.ctx.bot_msg.edit(view=self)

    @discord.ui.button(label="farmside", style=discord.ButtonStyle.green)
    async def farmside(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.conf["world"] = "farmside"
        # await interaction.response.send_message("farmside selected.",ephemeral=True)
        await self.wall_phase()
        await interaction.response.edit_message(embed=await self.build_embed())

    @discord.ui.button(label="metropolis", style=discord.ButtonStyle.gray)
    async def metropolis(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.conf["world"] = "metropolis"
        # await interaction.response.send_message("metropolis selected.",ephemeral=True)
        await self.wall_phase()
        await interaction.response.edit_message(embed=await self.build_embed())

    @discord.ui.button(label="underworld", style=discord.ButtonStyle.red)
    async def underworld(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.conf["world"] = "underworld"
        # await interaction.response.send_message("underworld selected.",ephemeral=True)
        await self.wall_phase()
        await interaction.response.edit_message(embed=await self.build_embed())
