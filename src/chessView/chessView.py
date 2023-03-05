import discord
from discord.ui import View

class InitChessGame(View):
    def __init__(self, ctx, opener, responder):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.opener = opener
        self.responder = responder
        self.mode = None

        self.responder_name = self.responder

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(content=":x: **__Duel timed out !__** :x:\nIf you want to start a chess game, please use the **/chess** command again !", view=self)

    async def select_opponent(self, select, interaction):
        await interaction.response.defer()

    @discord.ui.select(placeholder="Choose a mode", options=[
        discord.SelectOption(label="Blitz (5 minutes)", emoji="⚡", value="blitz"),
        discord.SelectOption(label="Rapid (10 minutes)", emoji="🚀", value="rapid"),
        discord.SelectOption(label="Classical (15 minutes)", emoji="🕰️", value="classical"),
    ])

    async def select_mode(self, select, interaction):
        self.mode = select.values[0]
        await interaction.response.defer()
        
    @discord.ui.button(label="Confirm", emoji="✔️", style=discord.ButtonStyle.green)
    async def confirm(self, button, interaction):
        if self.mode is None:
            await interaction.response.send_message("You need to select a mode !", ephemeral=True)
        else:
            await interaction.response.send_message(f"Your opponent is {self.responder} and you selected the {self.mode} mode !\n🪛**WIP**🪛", ephemeral=True)