import os
import discord
from discord.ext import commands
from storeDatas import *
from quotesHandler import getQuote
from quotesHandler import generateRandomIntForQuote
from dotenv import load_dotenv

# Created by Djason Gadiou (Magicred1#3948) on Discord
# Github : https://github.com/Magicred-1/self-improvement-bot
# This bot is made to help you workout by counting your push ups, pull ups and squats
# You we be able to add or remove points to other users (admin only)
# You will be able to reset your score (admin only)
# You will be able to see the leaderboard of the entire server.
# You will be able to see your score
# Do some push-ups, pull-ups and squats and get fit !
# For any questions, contact me on Discord (Magicred1#3948)

# List of quotes of Andrew Tate
quotes = getQuote("quotes.txt")

# Discord stuff
# Loads the token and the channel id from the .env file
load_dotenv()
TOKEN = os.getenv("token")
CHANNEL = os.getenv("channel")

COOLDOWN = 10  # Cooldown for the commands in seconds

initLeaderboard()


client = commands.Bot(command_prefix="!", intents=discord.Intents.all())  # The bot's prefix is "!" to call a command

# Bot commands logs and error handling
@client.event
async def on_command(ctx):
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    discordServerID = ctx.guild.id

    if not os.path.exists("logs"):
        os.makedirs("logs")

    logs_file = open(f"./logs/{date}-{discordServerID}.logs", "a")
    logs_file.write(
            f"{ctx.author} has used the command {ctx.message.content} in {ctx.channel} at {ctx.message.created_at}.\n"
        )
    logs_file.close()

# Error handling
@client.event
async def on_command_error(ctx, error):
    # If the command doesn't exist, we send this message
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
                ":x: This command doesn't exist, nice try .. :x:"
            )
    # If the user is on cooldown, we send this message
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
                f"Not too quick Gym Rat ! Wait {round(error.retry_after, 2)} seconds before using this command again ! :moyai:"
            )
    # If the user doesn't have the permissions to use this command, we send this message
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(
                f":x: You don't have the permissions to use this command ! :x:"
        )
    # If the user send a message in the wrong channel
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(
                f":x: You can't use this command in this channel ! :x:"
        )


@client.event
async def on_ready():
    # Prints the bot's name
    print(
        f"{client.user} (id : {client.user.id}) has connected to the Discord and he's here to make you workout and rich !"
    )


@client.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def pushups(ctx, number_of_pushups: int = 0):
    if ctx.channel.id == int(CHANNEL):
        # Adds the number of push-ups done by the user to the leaderboard
        if number_of_pushups > 0 and number_of_pushups <= 1000:
            await ctx.send(
                f"{ctx.author.name} has done {number_of_pushups} push-ups ! :partying_face:"
            )
            # We store the number of push-ups in the leaderboard.json file
            updateLeaderboard(ctx.author.name, "pushups", number_of_pushups)
        else:
            error = discord.Embed(
                title="You can't do 0 or negative squats or higher than 1000 ! Brookie !",
                color=discord.Colour.dark_red(),
            )
            error.set_image(
                url="https://media.tenor.com/1N_B-Tw_77QAAAAM/andrew-tate-shut-up.gif"
            )
            error.set_author(name=f"{ctx.author.name}")
            return await ctx.send(embed=error)


@client.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def pullups(ctx, number_of_pullups: int = 0):
    if ctx.channel.id == int(CHANNEL):
        # Adds the number of pull-ups done by the user to the leaderboard
        if number_of_pullups > 0 and number_of_pullups <= 1000:
            await ctx.send(
                f"{ctx.author.name} has done {number_of_pullups} pull-ups ! :partying_face:"
            )
            # We store the number of pull-ups multiplied by 2 in the leaderboard.json file
            updateLeaderboard(ctx.author.name, "pullups", number_of_pullups)
        else:
            error = discord.Embed(
                title="You can't do 0 or negative squats or higher than 1000 ! Brookie !",
                color=discord.Colour.dark_red(),
            )
            error.set_image(
                url="https://media.tenor.com/1N_B-Tw_77QAAAAM/andrew-tate-shut-up.gif"
            )
            error.set_author(name=f"{ctx.author.name}")
            return await ctx.send(embed=error)


@client.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def squats(ctx, number_of_squats: int = 0):
    if ctx.channel.id == int(CHANNEL):
        # We divide the number of squats by 5 because it's easier to do 5 squats than 1 push-up
        if number_of_squats > 0 and number_of_squats <= 1000:
            await ctx.send(
                f"{ctx.author.name} has done {number_of_squats} squats, keep going ! :partying_face:"
            )
            # We store the number of squats divided by 5 in the leaderboard.json file
            updateLeaderboard(ctx.author.name, "squats", number_of_squats)
        else:
            error = discord.Embed(
                title="You can't do 0 or negative squats or higher than 1000 ! Brookie !",
                color=discord.Colour.dark_red(),
            )
            error.set_image(
                url="https://media.tenor.com/1N_B-Tw_77QAAAAM/andrew-tate-shut-up.gif"
            )
            error.set_author(name=f"{ctx.author.name}")
            return await ctx.send(embed=error)

@client.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def score(ctx, username: str = None):
    if ctx.channel.id == int(CHANNEL):
        if username is None:
            username = ctx.author.name
        
        leaderboard = getLeaderboard()

        # Sends the user's score to the channel
        score_window = discord.Embed(
            title=":stars: **__Your score__** :stars:",
            description="**Reminder :**\n1 push-up = **1 point** / 1 pull-up = **2 points** / 5 squats = **1 point**",
            color=discord.Colour.random(),
        )
        score_window.set_author(name=f"{username}")
        score_window.set_thumbnail(
            url="https://media.tenor.com/BrHJBHqAxWAAAAAM/andrew-tate-top-g.gif"
        )
        
        # If the user is in the leaderboard and has done at least one exercise

        if username in leaderboard and getUserScore(username) > 0:
            score_window.add_field(
                name="**:hand_splayed: Push-ups : :hand_splayed:**",
                value=f"{leaderboard[username]['pushups']} push-ups",
                inline=True,
            )
            score_window.add_field(
                name="**:muscle: Pull-ups : :muscle:**",
                value=f"{leaderboard[username]['pullups']} pull-ups",
                inline=True,
            )
            score_window.add_field(
                name="**:leg: Squats : :leg:**",
                value=f"{leaderboard[username]['squats']} squats",
                inline=True,
            )
            score_window.add_field(
                name="**Total :**",
                value=f"{leaderboard[username]['pushups'] + leaderboard[username]['pullups'] + leaderboard[username]['squats']} points",
                inline=False,
            )
            await ctx.send(embed=score_window)
        else:
            score_window.add_field(
                name="You did no exercises ..", value="Your score is **0**, Brookie !\nHealth is Wealth use the command **__!get_started__** to start your journey !", inline=True
            )
            await ctx.send(embed=score_window)



@client.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def get_started(ctx):
    if ctx.channel.id == int(CHANNEL):
        # Sends the help message to the channel
        help = discord.Embed(
            title=":robot: **__Commands available :__** :robot:",
            color=discord.Colour.blue(),
        )
        help.add_field(
            name="**!score**", value="Shows your personnal score", inline=False
        )
        help.add_field(
            name="**!pushups <number>**",
            value="Adds the number of push-ups you have done to your score",
            inline=False,
        )
        help.add_field(
            name="**!pullups <number>**",
            value="Adds the number of pull-ups you have done to your score",
            inline=False,
        )
        help.add_field(
            name="**!squats <number>**",
            value="Adds the number of squats you have done to your score",
            inline=False,
        )
        help.add_field(
            name="**!leaderboard**",
            value="Shows the leaderboard of the server",
            inline=False,
        )
        help.add_field(name="**!quote**", value="Send a quote.", inline=False)
        help.add_field(
            name="**!topG**", value="Shows the TOP G OF THE MONTH", inline=False
        )
        help.add_field(name="**!avatar**", value="Shows your avatar", inline=False)
        help.add_field(
            name="**!get_started**", value="Shows the help message", inline=False
        )
        help.add_field(
            name="**!help_admin**",
            value="Admins only : Show the admins commands",
            inline=False,
        )
        help.set_image(
            url="https://media.tenor.com/x_30tXZ_DRQAAAAM/tate-andrew-tate.gif"
        )

        return await ctx.send(embed=help)


@client.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def quote(ctx):
    if ctx.channel.id == int(CHANNEL):
        # Sends one random quote from Andrew Tate to the channel
        andrewGIF = discord.Embed(
            title="Andrew Tate - The Top G",
            description="Quotes from Andrew Tate and more ...",
            color=discord.Colour.random(),
        )
        andrewGIF.add_field(
            name="**Quote of the day :**",
            value=f"{quotes[generateRandomIntForQuote()]}",
            inline=False,
        )
        andrewGIF.set_image(
            url="https://media.tenor.com/xSfy4B1dbrsAAAAM/cobra-tate-cobra.gif"
        )
        return await ctx.send(embed=andrewGIF)


@client.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def leaderboard(ctx):  # Shows the leaderboard
    if ctx.channel.id == int(CHANNEL):
        # Sends the leaderboard to the channel
        numberUser = 0
        if len(getLeaderboard()) == 0:
            return await ctx.send(
                ":x: No one has done any workout yet ! Do some push-ups, pull-ups and squats to get started ! :x:"
            )
        else:
            ranking_embed = discord.Embed(
                title=":moyai: **__Leaderboard - TOP 10 only__** :moyai:",
                description="**Reminder :**\n1 push-up = **1 point** / 1 pull-up = **2 points** / 5 squats = **1 point**",
                color=discord.Colour.random(),
            )
            leaderboard = getLeaderboard()
            ranking_embed.add_field(
                name="**__Discord Server Cumulated Score :__**",
                value=f"{getTotalScore()} points",
                inline=False,
            )
            ranking_embed.add_field(name="**__Ladder : __**", value="", inline=False)
            ranking_embed.set_image(
                url="https://media.discordapp.net/attachments/553215505712807938/826206690399617044/finna-pnut.gif"
            )
            # we use getUserScore() to sort the leaderboard by user's score
            foreachUser = sorted(
                leaderboard, key=lambda x: getUserScore(x), reverse=True
            )
            # we use the foreachUser list to get the user's score
            for user in foreachUser:
                if user == "TOP_G_OF_MONTH" or user == "Admin":
                    continue
                if numberUser <= 10 and getUserScore(user) > 0:
                    if user == foreachUser[0]:
                        ranking_embed.add_field(
                            name=f":crown: {user} :",
                            value=f"{getUserScore(user)} points",
                            inline=False,
                        )
                    elif user == foreachUser[1]:
                        ranking_embed.add_field(
                            name=f":second_place: {user} :",
                            value=f"{getUserScore(user)} points",
                            inline=False,
                        )
                    elif user == foreachUser[2]:
                        ranking_embed.add_field(
                            name=f":third_place: {user} :",
                            value=f"{getUserScore(user)} points",
                            inline=False,
                        )
                    else:
                        ranking_embed.add_field(
                            name=f"{numberUser+1} - {user} :",
                            value=f"{getUserScore(user)} points",
                            inline=False,
                        )
                    numberUser += 1
                else:
                    break
            return await ctx.send(embed=ranking_embed)


@client.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def avatar(ctx):
    # Sends the avatar of the user who sent the message https://cdn.discordapp.com/avatars/..../{user_avatar}.png
    if ctx.channel.id == int(CHANNEL):
        avatar = discord.Embed(
            color=discord.Colour.random(), title=f"**__{ctx.author.name}'s Avatar :__**"
        )
        avatar.set_image(url=f"{ctx.author.avatar}.png")
        return await ctx.send(embed=avatar)


@client.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def topG(ctx):
    top_g = getTheTopG()
    top_g_embed = discord.Embed(
        title="TOP_G_OF_THE_MONTH :", color=discord.Colour.random()
    )
    top_g_embed.add_field(
        name=f":man_lifting_weights:{top_g}:man_lifting_weights:",
        value="",
        inline=False,
    )
    top_g_embed.set_image(url="https://cdn3.emoji.gg/emojis/9749-andrew-tate.png")
    top_g_embed.set_footer(text="Made by Andrew Tate")
    await ctx.send(embed=top_g_embed)


# /!\ Admin only commands /!\


@client.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
@commands.has_permissions(administrator=True)
async def help_admin(ctx):
    if ctx.channel.id == int(CHANNEL):
        # Sends the help message to the channel
        help = discord.Embed(
            title="Admin commands available :", color=discord.Colour.random()
        )
        help.add_field(
            name="**!reset_points <user>**",
            value="Resets the score of a user",
            inline=False,
        )
        help.add_field(
            name="**!add_points <user> <pushups> <pullups> <squats>**",
            value="Adds points to a user",
            inline=False,
        )
        help.add_field(
            name="**!remove_points <user> <pushups> <pullups> <squats>**",
            value="Removes points to a user",
            inline=False,
        )
        help.add_field(
            name="**!reset_leaderboard**",
            value="Resets the leaderboard",
            inline=False,
        )
        help.add_field(
            name="**!setTopG <user>**",
            value="Sets the TOP_G_OF_THE_MONTH",
            inline=False,
        )
        help.add_field(
            name="**!help_admin**",
            value="Shows all the admin commands available.",
            inline=False,
        )

        return await ctx.send(embed=help)


# Reset the points of a user
@client.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
@commands.has_permissions(administrator=True)
async def reset_points(ctx, reset_user_points: str = ""):
    if reset_user_points == "":
        return await ctx.send(f"Please specify a user to reset the score of !")

    if ctx.channel.id == int(CHANNEL):
        # Prompt the user to confirm the reset
        await ctx.send(
            f"Are you sure you want to reset the score of {reset_user_points} ? (y/n)"
        )

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        msg = await client.wait_for("message", check=check)
        if msg.content == "y":
            deleteUserLeaderboard(reset_user_points)
            await ctx.send(f"{reset_user_points} score has been reset !")
        else:
            return await ctx.send(
                f"The score of {reset_user_points} has not been reset !"
            )


# Add points to a user
@client.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
@commands.has_permissions(administrator=True)
async def add_points(
    ctx,
    add_user_points: str = "",
    add_pushups: int = 0,
    add_pullups: int = 0,
    add_squats: int = 0,
):

    if add_user_points == "":
        return await ctx.send(f"Please specify a user to add points to !")

    if ctx.channel.id == int(CHANNEL):
        # Get the number of push-ups, pull-ups and squats to add or if null set it to 0
        if add_pushups < 0:
            add_pushups = 0

        elif add_pullups < 0:
            add_pullups = 0

        elif add_squats < 0:
            add_squats = 0

        # Prompt the user to confirm the reset
        await ctx.send(
            f"Are you sure you want to add {add_pushups} push-ups, {add_pullups} pull-ups and {add_squats} squats to {add_user_points}'s score ? (y/n)"
        )

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        msg = await client.wait_for("message", check=check)

        if msg.content == "y":
            leaderboard = getLeaderboard()
            if add_user_points in leaderboard:
                # Add the points to the user in the leaderboard
                updateLeaderboard(add_user_points, "pushups", add_pushups)
                updateLeaderboard(add_user_points, "pullups", add_pullups)
                updateLeaderboard(add_user_points, "squats", add_squats)
                await ctx.send(
                    f"{add_user_points} has been added {add_pushups} push-ups, {add_pullups} pull-ups and {add_squats} squats !"
                )
            else:
                updateLeaderboard(add_user_points, "pushups", add_pushups)
                updateLeaderboard(add_user_points, "pullups", add_pullups)
                updateLeaderboard(add_user_points, "squats", add_squats)

                await ctx.send(
                    f"{add_user_points} has been added to the leaderboard with {add_pushups} push-ups, {add_pullups} pull-ups and {add_squats} squats !"
                )


# Reset the leaderboard
@client.command()
@commands.has_permissions(administrator=True)
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
async def reset_leaderboard(ctx):
    if ctx.channel.id == int(CHANNEL):
        # Prompt the user to confirm the reset
        await ctx.send(f"Are you sure you want to reset the leaderboard ? (y/n)")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        msg = await client.wait_for("message", check=check)

        if msg.content == "y":
            leaderboard = getLeaderboard()
            for user in leaderboard:
                if user == "TOP_G_OF_THE_MONTH" or user == "Admin":
                    continue
                deleteUserLeaderboard(user)
            await ctx.send(f"The leaderboard has been reset !")
        else:
            return await ctx.send(f"The leaderboard has not been reset !")


@client.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
@commands.has_permissions(administrator=True)
async def setTopG(ctx, top_g_user: str = ""):
    if top_g_user == "":
        return await ctx.send(
            f"Please specify a user to set as the TOP_G_OF_THE_MONTH !"
        )

    if ctx.channel.id == int(CHANNEL):
        # Prompt the user to confirm the reset
        await ctx.send(
            f"Are you sure you want to set {top_g_user} as the TOP_G_OF_THE_MONTH ? (y/n)"
        )

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        msg = await client.wait_for("message", check=check)

        if msg.content == "y":
            setTheTopG(top_g_user)
            await ctx.send(f"{top_g_user} is now the TOP_G_OF_THE_MONTH !")
        else:
            return await ctx.send(f"{top_g_user} is not the TOP_G_OF_THE_MONTH !")

# Remove points from a user
@client.command()
@commands.cooldown(1, COOLDOWN, commands.BucketType.user)
@commands.has_permissions(administrator=True)
async def remove_points(
    ctx,
    remove_user_points: str = "",
    remove_pushups: int = "",
    remove_pullups: int = "",
    remove_squats: int = "",
):
    if ctx.channel.id == int(CHANNEL):
        if remove_user_points == "":
            await ctx.send(f"You must specify a user !")
            return

        if remove_pushups <= 0:
            remove_pushups = 0

        elif remove_pullups <= 0:
            remove_pullups = 0

        elif remove_squats <= 0:
            remove_squats = 0

        # Prompt the user to confirm the reset
        await ctx.send(
            f"Are you sure you want to remove {remove_pushups} push-ups, {remove_pullups} pull-ups and {remove_squats} squats to {remove_user_points}'s score ? (y/n)"
        )

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        msg = await client.wait_for("message", check=check)
        if msg.content == "y":
            leaderboard = getLeaderboard()
            # Check if the user has points
            if remove_user_points in leaderboard:
                # Check if the user has enough points to remove
                if (
                    leaderboard[remove_user_points]["pushups"] >= remove_pushups
                    and leaderboard[remove_user_points]["pullups"] >= remove_pullups
                    and leaderboard[remove_user_points]["squats"] >= remove_squats
                ):
                    updateLeaderboard(
                        remove_user_points, "pushups", -remove_pushups
                    )
                    updateLeaderboard(
                        remove_user_points, "pullups", -remove_pullups
                    )
                    updateLeaderboard(remove_user_points, "squats", -remove_squats)
                else:
                    return await ctx.send(
                        f"{remove_user_points} does not have enough points to remove {remove_pushups} push-ups, {remove_pullups} pull-ups and {remove_squats} squats !"
                    )
            return await ctx.send(
                f"{remove_pushups} push-ups, {remove_pullups} pull-ups and {remove_squats} squats have been removed from {remove_user_points}'s score !"
            )
        else:
            return await ctx.send(
                f"No points have been removed from {remove_user_points}'s score !"
            )
    else:
        return await ctx.send(
            f"{ctx.author.name} is not an admin !\nOnly admins can remove points from a user !"
        )


client.run(TOKEN)
