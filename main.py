import os
import discord
from dotenv import load_dotenv

# Created by Djason Gadiou (Magicred1#3948) on Discord
# Github : https://github.com/Magicred-1/self-improvement-bot
# This bot is made to help you workout by counting your push ups, pull ups and squats
# WIP : You we be able to add or remove points to other users (admin only)
# WIP : You will be able to reset your score (admin only)
# You will be able to see the leaderboard of the entire server.

# Leaderboard with 3 columns the number of push-ups / pull ups / squats done by each user
leaderboard = {}

cumuled_leaderboard = {
    'pushups': 0,
    'pullups': 0,
    'squats': 0,
}

load_dotenv()

token = os.getenv('token')

client = discord.Client()

@client.event
async def on_ready():
    # Prints the bot's name when it connects to Discord with a GIF of a workout
    print(f'{client.user} has connected to Discord and he\'s here to make you workout !')

@client.event
async def on_message(message):
    # Prevents the bot from replying to itself
    if message.author == client.user:
        return
    
    # Push-ups count as 1 point
    if message.startswith('!pushup'):
        await message.channel.send('How many push ups did you do ?')
        if (message.author.name not in leaderboard):
            leaderboard[message.author.name][0] = 0
        leaderboard[message.author.name][0] += int(message.content[8:])
        cumuled_leaderboard['pushups'] += int(message.content[8:])
        await message.channel.send('{} did ' + message.content[8:] + ' push ups, keep going !'.format(message.author.name))

    # Pull-ups count as 2 points
    if message.startswith('!pullup'):
        await message.channel.send('How many pull ups did you do ?')
        if (message.author.name not in leaderboard):
            leaderboard[message.author.name][1] = 0
        leaderboard[message.author.name][1] += int(message.content[8:]) * 2
        cumuled_leaderboard['pullups'] += int(message.content[8:]) * 2
        await message.channel.send('{} did ' + message.content[8:] + ' pull ups, keep going !'.format(message.author.name))

    # 5 Squats count as 1 point
    if message.startswith('!squats'):
        await message.channel.send('How many squats did you do ?')
        if (message.author.name not in leaderboard):
            leaderboard[message.author.name][2] = 0
        leaderboard[message.author.name][2] += int(message.content[8:]) / 5
        cumuled_leaderboard['squats'] += int(message.content[8:]) / 5
        await message.channel.send('{} did ' + message.content[8:] + ' squats, keep going !'.format(message.author.name))

    # Leaderboard command => shows the culmulated score of entire server
    if message.startswith('!leaderboard'):
        await message.channel.send('Here\'s the leaderboard :')
        for items in cumuled_leaderboard:
            await message.channel.send(items)

    # Help commands
    if message.startswith('!help pushup'):
        await message.channel.send('Here\'s the list of commands :\n!pushup [number of push ups] : adds the number of push ups to your score\n!pullup [number of pull ups] : adds the number of pull ups to your score\n!squats [number of squats] : adds the number of squats to your score\n!leaderboard : shows the leaderboard\n!help pushup : shows the push up commands\n!admin help : shows the admin commands')

    # Admin commands
    if message.startswith('!admin help'):
        if (message.author.top_role.permissions.administrator == True):
            await message.channel.send('Here\'s the list of admin commands :\n!admin add [name] [push ups] [pull ups] [squats] : adds the number of push ups, pull ups and squats to the user\'s score\n!admin remove [name] [push ups] [pull ups] [squats] : removes the number of push ups, pull ups and squats to the user\'s score\n!admin reset [name] : resets the user\'s score')
        else:
            await message.channel.send('{} you don\'t have the permission to use this command ! DO SOME PUSH UPS !'.format(message.author.name))

    # Admin add command
    if message.startswith('!admin add'):
        if (message.author.top_role.permissions.administrator == True):
            if (message.content[11:] not in leaderboard):
                leaderboard[message.content[11:]] = [0, 0, 0]
            leaderboard[message.content[11:]][0] += int(message.content[13:])
            leaderboard[message.content[11:]][1] += int(message.content[15:]) * 2
            leaderboard[message.content[11:]][2] += int(message.content[17:]) / 5
            await message.channel.send('You added ' + message.content[13:] + ' push ups, ' + message.content[15:] + ' pull ups and ' + message.content[17:] + ' squats to ' + message.content[11:] + '\'s score !')
        else:
            await message.channel.send('{} you don\'t have the permission to use this command ! DO SOME PUSH UPS !'.format(message.author.name))

    # Admin remove command
    if message.startswith('!admin remove'):
        if (message.author.top_role.permissions.administrator == True):
            if (message.content[14:] not in leaderboard):
                leaderboard[message.content[14:]] = [0, 0, 0]
            leaderboard[message.content[14:]][0] -= int(message.content[16:])
            leaderboard[message.content[14:]][1] -= int(message.content[18:]) * 2
            leaderboard[message.content[14:]][2] -= int(message.content[20:]) / 5
            await message.channel.send('You removed ' + message.content[16:] + ' push ups, ' + message.content[18:] + ' pull ups and ' + message.content[20:] + ' squats to ' + message.content[14:] + '\'s score !')
        else:
            await message.channel.send('{} you don\'t have the permission to use this command ! DO SOME PUSH UPS !'.format(message.author.name))

    # Admin reset command
    if message.startswith('!admin reset'):
        if (message.author.top_role.permissions.administrator == True):
            message.channel.send('WIP : Soon !')
        else:
            await message.channel.send('{} you don\'t have the permission to use this command ! DO SOME PUSH UPS !'.format(message.author.name))
    
client.run(token)
