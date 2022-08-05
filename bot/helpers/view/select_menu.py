import discord


class WallSelector(discord.ui.Select):
    def __init__(self, conf):
        self.conf = conf
        options = [
            discord.SelectOption(label="barn", emoji="🟢", value="barn"),
            discord.SelectOption(label="magma", emoji="🟠", value="magma"),
            discord.SelectOption(label="concrete", emoji="⚫", value="concrete"),
        ]
        super().__init__(
            placeholder="Select a wall", max_values=1, min_values=1, options=options
        )

    async def callback(self, interaction: discord.Interaction):
        self.conf["wall"] = self.selected_options[0].value
        # await interaction.response.send_message(content=f"Your choice is {self.values[0]}!",ephemeral=True)
