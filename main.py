import os
from discord.ext import commands
import discord
import random
#TODO: from storeDatas import updateLeaderboardInCSVfile
#TODO: from storeDatas import getLeaderboardFromCSVfile
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

# Leaderboard with 3 columns the number of push-ups / pull ups / squats done by each user being pushed into it
leaderboard = {}

cumuled_leaderboard = {
    'pushups': 0,
    'pullups': 0,
    'squats': 0,
}

# To get the quotes from the quotes.txt file at the root of the project
def getQuote(filename):
    quotes = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.replace('"', '')
            line = line.replace(',', '')
            line = line.split(':')
            quotes[int(line[0])] = line[1]
    return quotes

# List of quotes of Andrew Tate 
quotes = getQuote('quotes.txt')

# To generate a random int for the selection of a quote in the dictionnary
def generateRandomIntForQuote():
    randomInt = random.randint(1, len(quotes))
    return randomInt

# Loads the token and the channel id from the .env file
load_dotenv()
TOKEN = os.getenv('token')
CHANNEL = os.getenv('channel')

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@client.event
async def on_ready():
    # Prints the bot's name
    print(f'{client.user} has connected to the Discord and he\'s here to make you workout and rich !')

@client.command()
async def pushups(ctx, number_of_pushups: int):
    if ctx.channel.id == int(CHANNEL):
        # Adds the number of push-ups done by the user to the leaderboard
        if number_of_pushups > 0 :
            leaderboard[ctx.author.name] = leaderboard.get(ctx.author.name, {'pushups': 0, 'pullups': 0, 'squats': 0})
            leaderboard[ctx.author.name]['pushups'] += number_of_pushups
            cumuled_leaderboard['pushups'] += number_of_pushups
            await ctx.send(f'{ctx.author.name} has done {number_of_pushups} push-ups !')
            #TODO: update_leaderboard_in_CSV_file('leaderboard.csv', [[ctx.author.name, number_of_pushups]])
        else:
            await ctx.send('You can\'t do 0 or negative push-ups !')

        
@client.command()
async def pullups(ctx, number_of_pullups: int):
    if ctx.channel.id == int(CHANNEL):
        # Adds the number of pull-ups done by the user to the leaderboard
        leaderboard[ctx.author.name] = leaderboard.get(ctx.author.name, {'pushups': 0, 'pullups': 0, 'squats': 0})
        if number_of_pullups > 0 :
            leaderboard[ctx.author.name]['pullups'] += number_of_pullups
            cumuled_leaderboard['pullups'] += number_of_pullups * 2
            await ctx.send(f'{ctx.author.name} has done {number_of_pullups} pull-ups !')
            #TODO: update_leaderboard_in_CSV_file('leaderboard.csv', [[ctx.author.name, number_of_pullups]])
        else:
            await ctx.send('You can\'t do 0 or negative pull-ups !')

@client.command()
async def squats(ctx, number_of_squats: int):
    if ctx.channel.id == int(CHANNEL):
        # Adds the number of squats done by the user to the leaderboard
        leaderboard[ctx.author.name] = leaderboard.get(ctx.author.name, {'pushups': 0, 'pullups': 0, 'squats': 0})
        # We divide the number of squats by 5 because it's easier to do 5 squats than 1 push-up
        if number_of_squats > 0 :
            leaderboard[ctx.author.name]['squats'] += number_of_squats
            cumuled_leaderboard['squats'] += number_of_squats / 5
            await ctx.send(f'{ctx.author.name} has done {number_of_squats} squats, keep going !')
            #TODO: update_leaderboard_in_CSV_file('leaderboard.csv', [[ctx.author.name, number_of_squats]])
        else:
            await ctx.send('You can\'t do 0 or negative squats !')

@client.command()
async def score(ctx):
    if ctx.channel.id == int(CHANNEL):
        # Sends the user's score to the channel
        score_window = discord.Embed(
            title="**Your score :**",
            description="**Reminder :**\n1 push-up = 1 point, 1 pull-up = 2 points, 1 squat = 1 point per 5 squats",
            color=discord.Colour.dark_red()
        )
        if ctx.author.name in leaderboard:
            score_window.add_field(name="**Push-ups (1 pts)**", value=f'{leaderboard[ctx.author.name]["pushups"]}', inline=False)
            score_window.add_field(name="**Pull-ups** (2 pts)", value=f'{leaderboard[ctx.author.name]["pullups"]}', inline=False)
            score_window.add_field(name="**Squats** (1 pts per 5)", value=f'{leaderboard[ctx.author.name]["squats"]}', inline=False)
            score_window.add_field(name="**Total**", value=f'{cumuled_leaderboard["pushups"] + cumuled_leaderboard["pullups"] + cumuled_leaderboard["squats"]}', inline=False)
            await ctx.send(embed=score_window)
        else:
            score_window.title = "Your score is 0 ..."
            score_window.add_field(name="*Nothing to see ..*", value=f'{ctx.author.name} has not done any workout yet ! \nDo some push-ups, pull-ups and squats to get started !\nYou brookie !', inline=False)
            score_window.set_image(url="https://media.tenor.com/uIhsR71l6HkAAAAC/dosomepushupsfinlaim.gif")
            await ctx.send(embed=score_window)

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
        help.add_field(name="**!get_started**", value="Shows the help message", inline=False)
        help.add_field(name="**!help_admin**", value="Admins only : Show the admins commands", inline=False)
        help.set_image(url="https://media.tenor.com/x_30tXZ_DRQAAAAM/tate-andrew-tate.gif")

        await ctx.send(embed=help)

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
        await ctx.send(embed=andrewGIF)

@client.command()
async def ranking(ctx):
    if ctx.channel.id == int(CHANNEL):
        # Sends the leaderboard to the channel
        if leaderboard == {}:
            await ctx.send('No one has done any workout yet ! Do some push-ups, pull-ups and squats to get started !')
            return
        else:
            leaderboard_list = []
            embed = discord.Embed(
                title="Ranking List",
                description="The ranking of the server !",
                color=discord.Colour.blue()
            )
            for user in leaderboard:
                leaderboard_list.append([user, leaderboard[user]['pushups'], leaderboard[user]['pullups'], leaderboard[user]['squats'], cumuled_leaderboard['pushups'] + cumuled_leaderboard['pullups'] + cumuled_leaderboard['squats']])
            leaderboard_list.sort(key=lambda x: x[4], reverse=True)
            for i in range(len(leaderboard_list)):
                embed.add_field(name=f'{i+1} - {leaderboard_list[i][0]}', value=f'Push-ups (1 points) : {leaderboard_list[i][1]}\nPull-ups (2 points) : {leaderboard_list[i][2]}\nSquats (5 for 1 point) : {leaderboard_list[i][3]}\nTotal score : {leaderboard_list[i][4]}', inline=False)
            await ctx.send(embed=embed)

# /!\ Admin only commands /!\

@client.command()
async def help_admin(ctx):
    if ctx.channel.id == int(CHANNEL):
        # Sends the help message to the channel
        if not ctx.author.guild_permissions.administrator:
            await ctx.send('You are not an admin !')
            return
        else:
            help = discord.Embed(
                title="Admin commands available :",
                color=discord.Colour.blue()
            )
            help.add_field(name="**!reset_points <user>**", value="Resets the score of a user", inline=False)
            help.add_field(name="**!add_points <user> <pushups> <pullups> <squats>**", value="Adds points to a user", inline=False)
            help.add_field(name="**!remove_points <user> <pushups> <pullups> <squats>**", value="Removes points to a user", inline=False)
            help.add_field(name="**!reset_leaderboard**", value="Resets the leaderboard", inline=False)
            help.add_field(name="**!help_admin**", value="Shows all the admin commands available.", inline=False)

            await ctx.send(embed=help)

# Reset the points of a user
@client.command()
async def reset_points(ctx):
    if ctx.channel.id == int(CHANNEL):
        reset_user_points = ctx.message.content.split(' ')[1]

        # Prompt the user to confirm the reset
        await ctx.send(f'Are you sure you want to reset the score of {reset_user_points} ? (y/n)')

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        msg = await client.wait_for('message', check=check)
        if msg.content == 'y':
                if ctx.author.guild_permissions.administrator:
                    leaderboard[reset_user_points] = {'pushups': 0, 'pullups': 0, 'squats': 0}
                    await ctx.send(f'{reset_user_points} has reset his score !')
                else:
                    await ctx.send(f'{ctx.author.name} is not an admin ! Only admins can reset their score !')
        else:
            await ctx.send(f'The score of {ctx.author.name} has not been reset !')

# Add points to a user
@client.command()
async def add_points(ctx):
    if ctx.channel.id == int(CHANNEL):
        add_user_points = ctx.message.content.split(' ')[1]
        # Get the number of push-ups, pull-ups and squats to add or if null set it to 0
        add_pushups = int(ctx.message.content.split(' ')[2]) if len(ctx.message.content.split(' ')) > 2 else 0
        add_pullups = int(ctx.message.content.split(' ')[3]) if len(ctx.message.content.split(' ')) > 3 else 0
        add_squats = int(ctx.message.content.split(' ')[4]) if len(ctx.message.content.split(' ')) > 4 else 0

        # Prompt the user to confirm the reset
        await ctx.send(f'Are you sure you want to add {add_pushups} push-ups, {add_pullups} pull-ups and {add_squats} squats to {add_user_points}\'s score ? (y/n)')

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        msg = await client.wait_for('message', check=check)
        if msg.content == 'y':
                if ctx.author.guild_permissions.administrator:
                    leaderboard[add_user_points] = leaderboard.get(add_user_points, {'pushups': 0, 'pullups': 0, 'squats': 0})
                    leaderboard[add_user_points]['pushups'] += add_pushups
                    leaderboard[add_user_points]['pullups'] += add_pullups
                    leaderboard[add_user_points]['squats'] += add_squats
                    await ctx.send(f'{add_pushups} push-ups, {add_pullups} pull-ups and {add_squats} squats have been added to {add_user_points}\'s score !')
                else:
                    await ctx.send(f'{ctx.author.name} is not an admin !\nOnly admins can add points to a user !')
        else:
            await ctx.send(f'No points have been added to {add_user_points}\'s score !')

# Reset the leaderboard
@client.command()
async def reset_leaderboard(ctx):
    # Prompt the user to confirm the reset
    await ctx.send(f'Are you sure you want to reset the leaderboard ? (y/n)')

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    msg = await client.wait_for('message', check=check)
    if msg.content == 'y':
            if ctx.author.guild_permissions.administrator:
                leaderboard.clear()
                cumuled_leaderboard['pushups'] = 0
                cumuled_leaderboard['pullups'] = 0
                cumuled_leaderboard['squats'] = 0
                await ctx.send(f'The leaderboard has been reset !')
            else:
                await ctx.send(f'{ctx.author.name} is not an admin !\nOnly admins can reset the leaderboard !')
    else:
        await ctx.send(f'The leaderboard has not been reset !')

# Remove points from a user
@client.command()
async def remove_points(ctx):
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
                if ctx.author.guild_permissions.administrator:
                    leaderboard[remove_user_points] = leaderboard.get(remove_user_points, {'pushups': 0, 'pullups': 0, 'squats': 0})
                    leaderboard[remove_user_points]['pushups'] -= remove_pushups
                    leaderboard[remove_user_points]['pullups'] -= remove_pullups
                    leaderboard[remove_user_points]['squats'] -= remove_squats
                    await ctx.send(f'{remove_pushups} push-ups, {remove_pullups} pull-ups and {remove_squats} squats have been removed from {remove_user_points}\'s score !')
                else:
                    await ctx.send(f'{ctx.author.name} is not an admin !\nOnly admins can remove points from a user !')
        else:
            await ctx.send(f'No points have been removed from {remove_user_points}\'s score !')

client.run(TOKEN)
