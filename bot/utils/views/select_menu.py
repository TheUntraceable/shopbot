import discord


class WallSelector(discord.ui.Select):
    def __init__(self, view, conf):
        self._view = view
        self.conf = conf
        view.add_item(WallInfoButton())
        options = [
            discord.SelectOption(label="farm", emoji="🟢", value="farm"),
            discord.SelectOption(label="nether", emoji="🟠", value="nether"),
            discord.SelectOption(label="city", emoji="⚫", value="city"),
        ]
        super().__init__(
            placeholder="Select a wall", max_values=1, min_values=1, options=options
        )

    async def callback(self, interaction: discord.Interaction):
        self._view.conf["wall"] = self.values[0]
        embed, img = await self.view.build_embed()
        await interaction.response.edit_message(attachments=img, embed=embed)
        await self.view.roof_phase()


class WallInfoButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="select wall 🧱", style=discord.ButtonStyle.grey, disabled=True
        )


class RoofSelector(discord.ui.Select):
    def __init__(self, view, conf):
        self._view = view
        self.conf = conf
        view.add_item(RoofInfoButton())
        options = [
            discord.SelectOption(label="farm", emoji="🟢", value="farm"),
            discord.SelectOption(label="nether", emoji="🟠", value="nether"),
            discord.SelectOption(label="city", emoji="⚫", value="city"),
        ]
        super().__init__(
            placeholder="Select a roof", max_values=1, min_values=1, options=options
        )

    async def callback(self, interaction: discord.Interaction):
        self._view.conf["roof"] = self.values[0]
        embed, img = await self.view.build_embed()
        await interaction.response.edit_message(attachments=img, embed=embed)
        await self.view.top_phase()


class RoofInfoButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="select roof 🛖", style=discord.ButtonStyle.grey, disabled=True
        )


class TopSelector(discord.ui.Select):
    def __init__(self, view, conf):
        self._view = view
        self.conf = conf
        view.add_item(TopInfoButton())
        options = [
            discord.SelectOption(label="farm", emoji="🟢", value="farm"),
            discord.SelectOption(label="nether", emoji="🟠", value="nether"),
            discord.SelectOption(label="city", emoji="⚫", value="city"),
        ]
        super().__init__(
            placeholder="Select a top", max_values=1, min_values=1, options=options
        )

    async def callback(self, interaction: discord.Interaction):
        self._view.conf["top"] = self.values[0]
        embed, img = await self.view.build_embed()
        await interaction.response.edit_message(attachments=img, embed=embed)


class TopInfoButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="select top 🐙", style=discord.ButtonStyle.grey, disabled=True
        )
