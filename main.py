import os
from discord.ext import commands
import discord
import random
from dotenv import load_dotenv

# Created by Djason Gadiou (Magicred1#3948) on Discord
# Github : https://github.com/Magicred-1/self-improvement-bot
# This bot is made to help you workout by counting your push ups, pull ups and squats
# WIP : You we be able to add or remove points to other users (admin only)
# WIP : You will be able to reset your score (admin only)
# WIP : You will be able to see the leaderboard of the entire server.

# Leaderboard with 3 columns the number of push-ups / pull ups / squats done by each user
leaderboard = {}

cumuled_leaderboard = {
    'pushups': 0,
    'pullups': 0,
    'squats': 0,
}

# List of quotes of Andrew Tate 
quotes = {
    1: "The hallmark of a real man is controlling himself, controlling his emotions, and acting appropriately regardless of how he feels.",
    2: "Depression is not real. Feeling depressed is real. So, you can feel depressed, but you feel depressed and that is a natural, biological, evolutionary trigger for you to change something in your life.",
    3: "You can do it",
    4: "You are not a victim. You are a victor. You are a survivor. You are a warrior. You are a champion.",
    5: "Don't being a brokie, don't some pushups and grind",
    6: "Skinny little bitch - Cbum",
}

# To generate a random int for the selection of a quote in the dictionnary
def generateRandomIntForQuote():
    res = random.randint(1, len(quotes))
    return res

# Loads the token and the channel id from the .env file
load_dotenv()
TOKEN = os.getenv('token')
CHANNEL = os.getenv('channel')

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@client.event
async def on_ready():
    # Prints the bot's name
    print(f'{client.user} has connected to Discord and he\'s here to make you workout !\nType !help pushup to see the list of commands !')

@client.command()
async def pushups(ctx, number_of_pushups: int):
    # Adds the number of push-ups done by the user to the leaderboard
    leaderboard[ctx.author.name] = leaderboard.get(ctx.author.name, {'pushups': 0, 'pullups': 0, 'squats': 0})
    leaderboard[ctx.author.name]['pushups'] += number_of_pushups
    cumuled_leaderboard['pushups'] += number_of_pushups
    await ctx.send(f'{ctx.author.name} has done {number_of_pushups} push-ups !')

@client.command()
async def pullups(ctx, number_of_pullups: int):
    # Adds the number of pull-ups done by the user to the leaderboard
    leaderboard[ctx.author.name] = leaderboard.get(ctx.author.name, {'pushups': 0, 'pullups': 0, 'squats': 0})
    leaderboard[ctx.author.name]['pullups'] += number_of_pullups
    cumuled_leaderboard['pullups'] += number_of_pullups * 2
    await ctx.send(f'{ctx.author.name} has done {number_of_pullups} pull-ups !')

@client.command()
async def squats(ctx, number_of_squats: int):
    # Adds the number of squats done by the user to the leaderboard
    leaderboard[ctx.author.name] = leaderboard.get(ctx.author.name, {'pushups': 0, 'pullups': 0, 'squats': 0})
    leaderboard[ctx.author.name]['squats'] += number_of_squats
    cumuled_leaderboard['squats'] += number_of_squats / 5
    await ctx.send(f'{ctx.author.name} has done {number_of_squats} squats, keep going !')

@client.command()
async def score(ctx):
    # Sends the user's score to the channel
    if ctx.author.name in leaderboard:
        await ctx.send(f'{ctx.author.name} has done {leaderboard[ctx.author.name]["pushups"]} push-ups, {leaderboard[ctx.author.name]["pullups"]} pull-ups and {leaderboard[ctx.author.name]["squats"]} squats !\nTotal score : {cumuled_leaderboard["pushups"] + cumuled_leaderboard["pullups"] + cumuled_leaderboard["squats"]}')
    else:
        await ctx.send(f'{ctx.author.name} has not done any workout yet ! Do some push-ups, pull-ups and squats to get started !')

@client.command()
async def get_started(ctx):
    # Sends the help message to the channel
    await ctx.send('**__Getting Started :__**\n**!score** : Shows your score\n**!pushups <number>** : Adds the number of push-ups you have done to your score\n**!pullups <number>** : Adds the number of pull-ups you have done to your score\n**!squats <number>** : Adds the number of squats you have done to your score\n**!leaderboard** : Shows the leaderboard of the server')

@client.command()
async def quote(ctx):
    # Sends one random quote from Andrew Tate to the channel
    await ctx.send(f':muscle: **__Quote of the day :__** :muscle:\n{quotes[generateRandomIntForQuote()]}')

# Admin only commands

# Reset the points of a user
@client.command()
async def reset_points(ctx):
    # Resets the user's score to 0
    # Prompt the user to confirm the reset
    await ctx.send(f'Are you sure you want to reset your score ? (y/n)')
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    msg = await client.wait_for('message', check=check)
    if msg.content == 'y':
            if ctx.author.guild_permissions.administrator:
                leaderboard[ctx.author.name] = {'pushups': 0, 'pullups': 0, 'squats': 0}
                await ctx.send(f'{ctx.author.name} has reset his score !')
            else:
                await ctx.send(f'{ctx.author.name} is not an admin ! Only admins can reset their score !')
    else:
        await ctx.send(f'The score of {ctx.author.name} has not been reset !')

# Reset the

client.run(TOKEN)
