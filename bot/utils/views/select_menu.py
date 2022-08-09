import discord


class WallSelector(discord.ui.Select):
    def __init__(self, view, conf,up):
        self._view = view
        self.conf = conf
        view.add_item(WallInfoButton())
        options = []
        for i in up["wall"]:
            options.append(discord.SelectOption(label=i, emoji="🟢", value=i))
        super().__init__(
            placeholder="Select a wall", max_values=1, min_values=1, options=options
        )

    async def callback(self, interaction: discord.Interaction):
        self._view.conf["wall"] = self.values[0]
        embed, img = await self.view.build_embed()
        await interaction.response.edit_message(attachments=[img], embed=embed)
        await self.view.roof_phase()


class WallInfoButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="select wall 🧱", style=discord.ButtonStyle.grey, disabled=True
        )


class RoofSelector(discord.ui.Select):
    def __init__(self, view, conf,up):
        self._view = view
        self.conf = conf
        view.add_item(RoofInfoButton())
        options = []
        for i in up["roof"]:
            options.append(discord.SelectOption(label=i, emoji="🟢", value=i))
        super().__init__(
            placeholder="Select a roof", max_values=1, min_values=1, options=options
        )

    async def callback(self, interaction: discord.Interaction):
        self._view.conf["roof"] = self.values[0]
        embed, img = await self.view.build_embed()
        await interaction.response.edit_message(attachments=[img], embed=embed)
        await self.view.top_phase()


class RoofInfoButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="select roof 🛖", style=discord.ButtonStyle.grey, disabled=True
        )


class TopSelector(discord.ui.Select):
    def __init__(self, view, conf,up):
        self._view = view
        self.conf = conf
        view.add_item(TopInfoButton())
        options = []
        for i in up["top"]:
            options.append(discord.SelectOption(label=i, emoji="🟢", value=i))
        super().__init__(
            placeholder="Select a top", max_values=1, min_values=1, options=options
        )

    async def callback(self, interaction: discord.Interaction):
        self._view.conf["top"] = self.values[0]
        embed, img = await self.view.build_embed()
        await interaction.response.edit_message(attachments=[img], embed=embed)
        await self.view.save()


class TopInfoButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="select top 🐙", style=discord.ButtonStyle.grey, disabled=True
        )
