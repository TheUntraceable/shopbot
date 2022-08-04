import discord


class ShopCreate(discord.ui.View):
    def __init__(self,*,timeout:int=180):
        super().__init__(timeout=timeout)
        self.conf = {}
    
    async def build_embed(self):
        assets = {
            "farmside":"https://media.discordapp.net/attachments/1004758257707008050/1004758318855749732/farmside.png",
            "metropolis":"https://media.discordapp.net/attachments/1004758257707008050/1004758318209835008/metropolis.png",
            "underworld":"https://media.discordapp.net/attachments/1004758257707008050/1004758318553763870/underworld.png"
        }
        embed = discord.Embed(
            title=f"**~ welcome to the start of your journey ~**",
            color=0x2F3136
            )
        if self.conf.get("world"):
            embed.set_image(url=assets.get(self.conf["world"]))
        return embed
    
    @discord.ui.button(label="farmside",style=discord.ButtonStyle.green)
    async def farmside(
        self,
        interaction:discord.Interaction,
        _
        ):
        self.conf["world"] = "farmside"
        #await interaction.response.send_message("farmside selected.",ephemeral=True)
        await interaction.response.edit_message(embed=await self.build_embed())

    @discord.ui.button(label="metropolis",style=discord.ButtonStyle.gray)
    async def metropolis(
        self,
        interaction:discord.Interaction,
        _
        ):
        self.conf["world"] = "metropolis"
        #await interaction.response.send_message("metropolis selected.",ephemeral=True)
        await interaction.response.edit_message(embed=await self.build_embed())
    
    @discord.ui.button(label="underworld",style=discord.ButtonStyle.red)
    async def underworld(
        self,
        interaction:discord.Interaction,
        _
        ):
        self.conf["world"] = "underworld"
        #await interaction.response.send_message("underworld selected.",ephemeral=True)
        await interaction.response.edit_message(embed=await self.build_embed())