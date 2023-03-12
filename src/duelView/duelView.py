import discord
from discord.ui import View
import datetime
import asyncio

class InitDuel(View):
    def __init__(self, ctx, user, challenger):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.user = user
        self.challenger = challenger
        self.exercise = None
        self.time = None

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(content=":x: **__Duel timed out !__** :x:\nIf you want to start a duel, please use the **/duel** command again !", view=self)

    @discord.ui.select(
        placeholder="Select an exercise ...",
        options=[
                discord.SelectOption(
                    label="Push-ups",
                    description="Challenge someone to a push-up duel",
                    emoji="🖐️",
                    value="pushups",
                ),
                discord.SelectOption(
                    label="Pull-ups",
                    description="Challenge someone to a pull-up duel",
                    emoji="💪",
                    value="pullups",
                ),
                discord.SelectOption(
                    label="Squats",
                    description="Challenge someone to a squat duel",
                    emoji="🦵",
                    value="squats",
                ),
                discord.SelectOption(
                    label="Jumping Jacks",
                    description="Challenge someone to a Jumping Jacks duel",
                    emoji="👟",
                    value="jumping_jacks",
                ),
                discord.SelectOption(
                    label="Burpees",
                    description="Challenge someone to a burpee duel",
                    emoji="🆙",
                    value="burpees",
                ),
                discord.SelectOption(
                    label="Sit-ups",
                    description="Challenge someone to a sit-up duel",
                    emoji="🪑",
                    value="situps",
                ),  
            ])

    async def select_exercise(self, select: discord.ui.Select, interaction: discord.Interaction):
        self.exercise = select.values[0]
        await interaction.response.defer()

    @discord.ui.select(
        placeholder="Select a time ...",
        options=[
                discord.SelectOption(
                    label="1 minute",
                    description="Challenge someone to a 1 minute duel",
                    emoji="1️⃣",
                    value="1",
                ),
                discord.SelectOption(
                    label="2 minutes",
                    description="Challenge someone to a 2 minutes duel",
                    emoji="2️⃣",
                    value="2",
                ),
                discord.SelectOption(
                    label="3 minutes",
                    description="Challenge someone to a 3 minutes duel",
                    emoji="3️⃣",
                    value="3",
                ),
                discord.SelectOption(
                    label="5 minutes",
                    description="Challenge someone to a 5 minutes duel",
                    emoji="5️⃣",
                    value="5",
                ),
                discord.SelectOption(
                    label="10 minutes",
                    description="Challenge someone to a 10 minutes duel",
                    emoji="🔟",
                    value="10",
                ),
    ])
    async def select_time(self, select: discord.ui.Select, interaction: discord.Interaction):
        self.time = select.values[0]
        await interaction.response.defer()

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, emoji="✅")
    async def send(self, button: discord.ui.Button, interaction: discord.Interaction):
        # we check if the user if the user who clicked on the button is the same as the user who was challenged
        if self.exercise != None and self.time != None:
            await interaction.response.send_message(
                f"{self.user.mention} {self.challenger} challenged you to a {self.exercise} duel for {self.time} minute(s) !\nYou got 2 minutes to either **Accept** or **Decline** the duel !", 
                ephemeral=False, 
                view=RequestDuel(self.ctx, self.challenger, self.user, self.exercise, self.time)
            )
            print(f"A duel has been started !\n{self.challenger} challenged {self.user} to a {self.exercise} duel for {self.time} minutes !")
            self.stop()
        else:
            await interaction.response.send_message(
                f"{self.user.mention} Please select an exercise and a time !", ephemeral=True
            )


    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.blurple, emoji="❌")
    async def decline(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"You cancelled the duel request !", ephemeral=True
        )
        self.stop()

class RequestDuel(View):
    def __init__(self, ctx, challenger, user, exercise, time):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.user = user
        self.challenger = challenger
        self.exercise = exercise
        self.time = time

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(content=":x: **__Duel timed out !__** :x:\nIf you want to start a duel, please use the **/duel** command again !", view=self)

    @discord.ui.button(label="Accept Duel", style=discord.ButtonStyle.green, emoji="✅")
    async def accept(self, button: discord.ui.Button, interaction: discord.Interaction):
        # if it's the user that clicked on the button we send the message to the challenger
        if self.user == interaction.user:
            await interaction.response.send_message(
                f"{self.user.mention} **{self.challenger}** challenged you to a **{self.exercise}** duel for **{self.time}** minute(s) !", ephemeral=False, 
                view=StartDuel(self.ctx, self.user, self.exercise, self.time, self.challenger)
            )
            self.stop()
        else:
            embed = discord.Embed(
                title=":x: **__Nope !__** :x:",
                description=f"{interaction.user.mention} you can't accept a duel that is not yours !", 
                color=discord.Colour.random()
            )
            embed.set_image(url="https://media.tenor.com/BfMG_jjqB04AAAAd/andrew-tate-tate.gif")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Decline Duel", style=discord.ButtonStyle.blurple, emoji="❌")
    async def decline(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.user == interaction.user:
            await interaction.response.send_message(
                f"{self.user.mention} declined the duel !", ephemeral=True
            )
            self.stop()
        else:
            embed = discord.Embed(
                title=":x: **__Nope !__** :x:",
                description=f"{interaction.user.mention} you can't decline a duel that is not yours !", 
                color=discord.Colour.random()
            )
            embed.set_image(url="https://media.tenor.com/BfMG_jjqB04AAAAd/andrew-tate-tate.gif")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    async def on_timeout(self):
        await self.ctx.send(f"{self.user.mention} didn't accept the duel of {self.challenger} !")
        for child in self.children:
            child.disabled = True
        self.stop()


class StartDuel(View):
    def __init__(self, ctx, user, exercise, time, challenger):
        super().__init__(timeout=int(time) * 60 + 30)
        self.ctx = ctx
        self.user = user
        self.exercise = exercise
        self.time = time
        self.challenger = challenger
        self.timestamp = datetime.datetime.utcnow() + datetime.timedelta(minutes=int(time))
    

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(content=":x: **__Duel timed out !__** :x:\nIf you want to start a duel, please use the **/duel** command again !", view=self)

    async def startCountdown(self, time, timestamp):
        # remove the buttons
        self.clear_items()
        self.duel_embed = discord.Embed(
            title=f"**:crossed_swords: Fitness Duel :crossed_swords:**",
            description=f"{self.user.mention} vs {self.challenger}",
            color=discord.Colour.random(),
        )
        self.duel_embed.set_thumbnail(url="https://media.tenor.com/x5X7TBHrvzMAAAAM/fight.gif")
        self.duel_embed.add_field(
            name="**:hourglass: __Time :__ :hourglass:**",
            value=f"{time} minute(s)",
            inline=False,
        )
        self.duel_embed.add_field(
            name="**👊 __Exercise :__ 👊**",
            value=f"{self.exercise}",
            inline=False,
        )
        self.duel_embed.set_footer(text=f"Ends at {timestamp.utcnow() + datetime.timedelta(minutes=int(time))}")

        await self.ctx.send(embed=self.duel_embed, view=self)

        if timestamp > datetime.datetime.utcnow() + datetime.timedelta(minutes=int(time)):
            await asyncio.sleep(1)

            # update the embed
            self.duel_embed.set_field_at(
                0, name="**:hourglass: __Time :__ :hourglass:**", value=f"{time - 1} minute(s)"
            )
            
    @discord.ui.button(label="Start", style=discord.ButtonStyle.green)
    async def start(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user not in [self.user, self.challenger]:
            await interaction.response.send_message(
                f"You not that guy pal, trust me {interaction.user.mention} !", ephemeral=True
            )
        else:
            await interaction.message.delete()
            # start the countdown
            await self.startCountdown(self.time, self.timestamp)
            await asyncio.sleep(1)
            self.stop()
