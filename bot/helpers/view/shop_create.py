import discord


class ShopCreate(discord.ui.View):
    def __init__(self,*,timeout:int=180):
        super().__init__(timeout=timeout)
        self.conf = {}
    
    @discord.ui.button(label="farmside",style=discord.ButtonStyle.green)
    async def farmside(
        self,
        button:discord.ui.Button,
        interaction:discord.Interaction
        ):
        self.conf["world"] = "farmside"
        await interaction.response.edit_message(content=f"This is an edited button response!")

    @discord.ui.button(label="metropolis",style=discord.ButtonStyle.gray)
    async def metropolis(
        self,
        button:discord.ui.Button,
        interaction:discord.Interaction
        ):
        self.conf["world"] = "metropolis"
        await interaction.response.edit_message(content=f"This is an edited button response!")
    
    @discord.ui.button(label="underworld",style=discord.ButtonStyle.red)
    async def underworld(
        self,
        button:discord.ui.Button,
        interaction:discord.Interaction
        ):
        self.conf["world"] = "underworld"
        await interaction.response.edit_message(content=f"This is an edited button response!")