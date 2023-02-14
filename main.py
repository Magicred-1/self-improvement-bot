import os
import discord
from discord.ext import commands
from discord import Member
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
quotes = getQuote('quotes.txt')

# Discord stuff
# Loads the token and the channel id from the .env file
load_dotenv()
TOKEN = os.getenv('token')
CHANNEL = os.getenv('channel')

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@client.event
async def on_ready():
    # Prints the bot's name
    print(f'{client.user} (id : {client.user.id}) has connected to the Discord and he\'s here to make you workout and rich !')

@client.command()
async def pushups(ctx, number_of_pushups: int):
    if ctx.channel.id == int(CHANNEL):
        # Adds the number of push-ups done by the user to the leaderboard
        if number_of_pushups > 0 and number_of_pushups <= 1000:
            await ctx.send(f'{ctx.author.name} has done {number_of_pushups} push-ups !')
            # We store the number of push-ups in the leaderboard.json file
            updateLeaderboard(ctx.author.name, 'pushups', number_of_pushups)
        else:
            error = discord.Embed(
                title="You can't do 0 or negative squats or higher than 1000 ! Brookie !",
                color=discord.Colour.dark_red()
            )
            error.set_image(url="https://media.tenor.com/1N_B-Tw_77QAAAAM/andrew-tate-shut-up.gif")
            error.set_author(name=f'{ctx.author.name}')
            return await ctx.send(embed=error)

        
@client.command()
async def pullups(ctx, number_of_pullups: int):
    if ctx.channel.id == int(CHANNEL):
        # Adds the number of pull-ups done by the user to the leaderboard
        if number_of_pullups > 0 and number_of_pullups <= 1000:
            await ctx.send(f'{ctx.author.name} has done {number_of_pullups} pull-ups !')
            # We store the number of pull-ups multiplied by 2 in the leaderboard.json file
            updateLeaderboard(ctx.author.name, 'pullups', number_of_pullups)
        else:
            error = discord.Embed(
                title="You can't do 0 or negative squats or higher than 1000 ! Brookie !",
                color=discord.Colour.dark_red()
            )
            error.set_image(url="https://media.tenor.com/1N_B-Tw_77QAAAAM/andrew-tate-shut-up.gif")
            error.set_author(name=f'{ctx.author.name}')
            return await ctx.send(embed=error)

@client.command()
async def squats(ctx, number_of_squats: int):
    if ctx.channel.id == int(CHANNEL):
        # We divide the number of squats by 5 because it's easier to do 5 squats than 1 push-up
        if number_of_squats > 0 and number_of_squats <= 1000:
            await ctx.send(f'{ctx.author.name} has done {number_of_squats} squats, keep going !')
            # We store the number of squats divided by 5 in the leaderboard.json file
            updateLeaderboard(ctx.author.name, 'squats', number_of_squats)
        else:
            error = discord.Embed(
                title="You can't do 0 or negative squats or higher than 1000 ! Brookie !",
                color=discord.Colour.dark_red()
            )
            error.set_image(url="https://media.tenor.com/1N_B-Tw_77QAAAAM/andrew-tate-shut-up.gif")
            error.set_author(name=f'{ctx.author.name}')
            return await ctx.send(embed=error)

@client.command()
async def score(ctx):
    if ctx.channel.id == int(CHANNEL):
        # Sends the user's score to the channel
        score_window = discord.Embed(
            title=":muscle: **__Your score__** :muscle:",
            description="**Reminder :**\n1 push-up = **1 point** / 1 pull-up = **2 points** / 5 squats = **1 point**",
            color=discord.Colour.dark_red()
        )
        leaderboard = getLeaderboard()
        for user in leaderboard:
            if user == ctx.author.name and getUserScore(user) > 0:
                score_window.set_author(name=f'{ctx.author.name}')
                score_window.add_field(name=f'{user}\'s push-ups :', value=f'{leaderboard[user]["pushups"]} points', inline=False)
                score_window.add_field(name=f'{user}\'s pull-ups :', value=f'{leaderboard[user]["pullups"]} points', inline=False)
                score_window.add_field(name=f'{user}\'s squats :', value=f'{leaderboard[user]["squats"]} points', inline=False)
                score_window.add_field(name=f'{user}\'s total score :', value=f'{getUserScore(user)} points', inline=False)
                score_window.set_image(url="https://media.tenor.com/BrHJBHqAxWAAAAAM/andrew-tate-top-g.gif")
                return await ctx.send(embed=score_window)
        else:
            score_window.title = "Your score is 0 ..."
            score_window.add_field(name="*Nothing to see ..*", value=f'{ctx.author.name} has not done any workout yet ! \nDo some push-ups, pull-ups and squats to get started !\nYou brookie !', inline=False)
            score_window.set_image(url="https://media.tenor.com/uIhsR71l6HkAAAAC/dosomepushupsfinlaim.gif")
            return await ctx.send(embed=score_window)

@client.command()
async def get_started(ctx):
    if ctx.channel.id == int(CHANNEL):
        # Sends the help message to the channel
        help = discord.Embed(
            title="Commands available :",
            color=discord.Colour.blue()
        )
        help.add_field(name="**!score**", value="Shows your personnal score", inline=False)
        help.add_field(name="**!pushups <number>**", value="Adds the number of push-ups you have done to your score", inline=False)
        help.add_field(name="**!pullups <number>**", value="Adds the number of pull-ups you have done to your score", inline=False)
        help.add_field(name="**!squats <number>**", value="Adds the number of squats you have done to your score", inline=False)
        help.add_field(name="**!ranking**", value="Shows the leaderboard of the server", inline=False)
        help.add_field(name="**!quote**", value="Send a quote.", inline=False)
        help.add_field(name="**!topG**", value="Shows the TOP G OF THE MONTH", inline=False)
        help.add_field(name="**!avatar**", value="Shows your avatar", inline=False)
        help.add_field(name="**!get_started**", value="Shows the help message", inline=False)
        help.add_field(name="**!help_admin**", value="Admins only : Show the admins commands", inline=False)
        help.set_image(url="https://media.tenor.com/x_30tXZ_DRQAAAAM/tate-andrew-tate.gif")

        return await ctx.send(embed=help)

@client.command()
async def quote(ctx):
    if ctx.channel.id == int(CHANNEL):
        # Sends one random quote from Andrew Tate to the channel
        andrewGIF = discord.Embed(
                    title="Andrew Tate - The Top G",
                    description="Quotes from Andrew Tate and more ...",
                    color=discord.Colour.blue()
                )
        andrewGIF.add_field(name="**Quote of the day :**", value=f'{quotes[generateRandomIntForQuote()]}', inline=False)
        andrewGIF.set_image(url="https://media.tenor.com/xSfy4B1dbrsAAAAM/cobra-tate-cobra.gif")
        return await ctx.send(embed=andrewGIF)

@client.command()
async def ranking(ctx): # Shows the leaderboard todo : debug that shit
    if ctx.channel.id == int(CHANNEL):
        # Sends the leaderboard to the channel
        numberUser = 0
        if len(getLeaderboard()) == 0:
            return await ctx.send('No one has done any workout yet ! Do some push-ups, pull-ups and squats to get started !')
        else:
            ranking_embed = discord.Embed(
                title=":moyai: **__Ranking Leaderboard - TOP 10 only__** :moyai:",
                description="**Reminder :**\n1 push-up = **1 point** / 1 pull-up = **2 points** / 5 squats = **1 point**",
                color=discord.Colour.dark_red()
            )
            leaderboard = getLeaderboard()
            ranking_embed.add_field(name="**__Discord Cumulated Score :__**", value=f'{getTotalScore()} points', inline=False)
            ranking_embed.add_field(name="**__Ladder : __**", value="** **", inline=False)
            ranking_embed.set_image(url="https://media.discordapp.net/attachments/553215505712807938/826206690399617044/finna-pnut.gif")
            # we use getTotalscore() to sort the leaderboard
            foreachUser = sorted(leaderboard, key=lambda x: getUserScore(x), reverse=True)
            for user in foreachUser:
                if user == "TOP_G_OF_MONTH" or user == "Admin":
                    continue
                if numberUser <= 10 and getUserScore(user) > 0:
                    if user == foreachUser[0]:
                        ranking_embed.add_field(name=f':crown: {user} :', value=f'{getUserScore(user)} points', inline=False)
                    elif user == foreachUser[1]:
                        ranking_embed.add_field(name=f':second_place: {user} :', value=f'{getUserScore(user)} points', inline=False)
                    elif user == foreachUser[2]:
                        ranking_embed.add_field(name=f':third_place: {user} :', value=f'{getUserScore(user)} points', inline=False)
                    else:
                        ranking_embed.add_field(name=f'{numberUser+1} - {user} :', value=f'{getUserScore(user)} points', inline=False)
                    numberUser += 1
                else:
                    break
            return await ctx.send(embed=ranking_embed)

@client.command()
async def topG(ctx):
    top_g = getTheTopG()
    top_g_embed = discord.Embed(
        title="TOP_G_OF_THE_MONTH :",
        color=discord.Colour.yellow()
    )
    top_g_embed.add_field(name=f':man_lifting_weights:{top_g}:man_lifting_weights:', value="", inline=False)
    top_g_embed.set_image(url="https://media.discordapp.net/attachments/553215505712807938/826206690399617044/finna-pnut.gif")
    top_g_embed.set_footer(text="Made by Andrew Tate")
    await ctx.send(embed=top_g_embed)

# /!\ Admin only commands /!\

@client.command()
async def help_admin(ctx):
    if ctx.channel.id == int(CHANNEL):
        # Sends the help message to the channel
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send('You are not an admin !')
        else:
            help = discord.Embed(
                title="Admin commands available :",
                color=discord.Colour.blue()
            )
            help.add_field(name="**!reset_points <user>**", value="Resets the score of a user", inline=False)
            help.add_field(name="**!add_points <user> <pushups> <pullups> <squats>**", value="Adds points to a user", inline=False)
            help.add_field(name="**!remove_points <user> <pushups> <pullups> <squats>**", value="Removes points to a user", inline=False)
            help.add_field(name="**!reset_leaderboard**", value="Resets the leaderboard", inline=False)
            help.add_field(name="**!setTopG <user>**", value="Sets the TOP_G_OF_THE_MONTH", inline=False)
            help.add_field(name="**!help_admin**", value="Shows all the admin commands available.", inline=False)

            return await ctx.send(embed=help)

@client.command()
async def avatar(ctx):
    # Sends the avatar of the user who sent the message https://cdn.discordapp.com/avatars/{user_id}/{user_avatar}.png
    if ctx.channel.id == int(CHANNEL):
        avatar = discord.Embed(
            color=discord.Colour.blue()
        )
        avatar.add_field(name=f'{ctx.author.name}\'s avatar :', value="", inline=False)
        avatar.set_image(url=f"{ctx.author.avatar}.png")
        return await ctx.send(embed=avatar)

# Reset the points of a user
@client.command()
async def reset_points(ctx, reset_user_points):
    if ctx.author.guild_permissions.administrator:
        if ctx.channel.id == int(CHANNEL):
            # Prompt the user to confirm the reset
            await ctx.send(f'Are you sure you want to reset the score of {reset_user_points} ? (y/n)')

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            msg = await client.wait_for('message', check=check)
            if msg.content == 'y':
                deleteUserLeaderboard(reset_user_points)
                await ctx.send(f'{reset_user_points} score has been reset !')
            else:
                return await ctx.send(f'The score of {reset_user_points} has not been reset !')
    else:
        return await ctx.send(f'{ctx.author.name} is not an admin ! Only admins can reset their score !')

# Add points to a user
@client.command()
async def add_points(ctx, add_user_points, add_pushups, add_pullups, add_squats):
    if ctx.author.guild_permissions.administrator:
        if ctx.channel.id == int(CHANNEL):
            add_user_points = ctx.message.content.split(' ')[1] 
            # Get the number of push-ups, pull-ups and squats to add or if null set it to 0
            if add_user_points == "":
                await ctx.send(f'You must specify a user !')
                return
                
            if add_pushups < 0:
                add_pushups = 0

            if add_pullups < 0:
                add_pullups = 0

            if add_squats < 0:
                add_squats = 0


            # Prompt the user to confirm the reset
            await ctx.send(f'Are you sure you want to add {add_pushups} push-ups, {add_pullups} pull-ups and {add_squats} squats to {add_user_points}\'s score ? (y/n)')

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            msg = await client.wait_for('message', check=check)
            if msg.content == 'y':
                leaderboard = getLeaderboard()
                if add_user_points in leaderboard:
                    # Add the points to the user in the leaderboard
                    updateLeaderboard(add_user_points, "pushups", add_pushups)
                    updateLeaderboard(add_user_points, "pullups", add_pullups)
                    updateLeaderboard(add_user_points, "squats", add_squats)
                    await ctx.send(f'{add_user_points} has been added {add_pushups} push-ups, {add_pullups} pull-ups and {add_squats} squats !')
                else:
                    updateLeaderboard(add_user_points, "pushups", add_pushups)
                    updateLeaderboard(add_user_points, "pullups", add_pullups)
                    updateLeaderboard(add_user_points, "squats", add_squats)

                    await ctx.send(f'{add_user_points} has been added to the leaderboard with {add_pushups} push-ups, {add_pullups} pull-ups and {add_squats} squats !')
    else:
        return await ctx.send(f'{add_user_points} is not an admin !\nOnly admins can add points to a user !')

# Reset the leaderboard
@client.command()
async def reset_leaderboard(ctx):
    if ctx.author.guild_permissions.administrator:
        if ctx.channel.id == int(CHANNEL):
            # Prompt the user to confirm the reset
            await ctx.send(f'Are you sure you want to reset the leaderboard ? (y/n)')

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            msg = await client.wait_for('message', check=check)

            if msg.content == 'y':
                leaderboard = getLeaderboard()
                for user in leaderboard:
                    if user == "TOP_G_OF_THE_MONTH" or user == "Admin":
                        continue
                    deleteUserLeaderboard(user)
                await ctx.send(f'The leaderboard has been reset !')
            else:
                return await ctx.send(f'The leaderboard has not been reset !')
    else:
        return await ctx.send(f'{ctx.author.name} is not an admin !\nOnly admins can reset the leaderboard !')

@client.command()
async def setTopG(ctx, top_g_user):
    if ctx.author.guild_permissions.administrator:
        if ctx.channel.id == int(CHANNEL):
            # Prompt the user to confirm the reset
            await ctx.send(f'Are you sure you want to set {top_g_user} as the TOP_G_OF_THE_MONTH ? (y/n)')

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            msg = await client.wait_for('message', check=check)
            if msg.content == 'y':
                setTheTopG(top_g_user)
                await ctx.send(f'{top_g_user} is now the TOP_G_OF_THE_MONTH !')
            else:
                return await ctx.send(f'{top_g_user} is not the TOP_G_OF_THE_MONTH !')
    else:
        return await ctx.send(f'{ctx.author.name} is not an admin !\nOnly admins can set the TOP_G_OF_THE_MONTH !')

# Remove points from a user
@client.command()
async def remove_points(ctx):
    if ctx.author.guild_permissions.administrator:
        if ctx.channel.id == int(CHANNEL):
            remove_user_points = ctx.message.content.split(' ')[1]
            # Get the number of push-ups, pull-ups and squats to add or if null set it to 0
            remove_pushups = int(ctx.message.content.split(' ')[2]) if len(ctx.message.content.split(' ')) > 2 else 0
            remove_pullups = int(ctx.message.content.split(' ')[3]) if len(ctx.message.content.split(' ')) > 3 else 0
            remove_squats = int(ctx.message.content.split(' ')[4]) if len(ctx.message.content.split(' ')) > 4 else 0

            # Prompt the user to confirm the reset
            await ctx.send(f'Are you sure you want to remove {remove_pushups} push-ups, {remove_pullups} pull-ups and {remove_squats} squats to {remove_user_points}\'s score ? (y/n)')

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            msg = await client.wait_for('message', check=check)
            if msg.content == 'y':
                        leaderboard = getLeaderboard()
                        # Check if the user has points
                        if remove_user_points in leaderboard:
                            # Check if the user has enough points to remove
                            if leaderboard[remove_user_points]['pushups'] >= remove_pushups and leaderboard[remove_user_points]['pullups'] >= remove_pullups and leaderboard[remove_user_points]['squats'] >= remove_squats:
                                updateLeaderboard(remove_user_points, "pushups", -remove_pushups)
                                updateLeaderboard(remove_user_points, "pullups", -remove_pullups)
                                updateLeaderboard(remove_user_points, "squats", -remove_squats)
                            else:
                                return await ctx.send(f'{remove_user_points} does not have enough points to remove {remove_pushups} push-ups, {remove_pullups} pull-ups and {remove_squats} squats !')
                        return await ctx.send(f'{remove_pushups} push-ups, {remove_pullups} pull-ups and {remove_squats} squats have been removed from {remove_user_points}\'s score !')
            else:
                return await ctx.send(f'No points have been removed from {remove_user_points}\'s score !')
    else:
        return await ctx.send(f'{ctx.author.name} is not an admin !\nOnly admins can remove points from a user !')

client.run(TOKEN)
