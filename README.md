# self-improvement-bot
## Andrew Tate's self-improvement bot (Discord bot) using Python and Discord.py
**By: [Djason Gadiou](https://github.com/Magicred-1/)**

**Discord: Magicred1#3948**

This is a simple Discord bot that will help you to improve yourself. 
It will help you to keep track of your progress and motivate you to do more. 
It will also give you a random quote from Andrew Tate and other inspirationnal people to keep you motivated and help you to improve yourself.

## How to set up and use it ?

1. Clone this repository
2. Install the requirements with `pip install -r requirements.txt` with MacOS / Linux distro or `py -3 -m pip install -r requirements.txt` on Windows.
3. Rename the file `.env.example` to `.env`
4. Add your discord **bot token** in the `.env` file and the **channel id** where you want the bot to send the messages.
5. Run `py -3 main.py` in the terminal from folder where the bot is located.

If you want to use the bot on your own server, you will need to create a Discord bot and add it to your server.
Here is a tutorial on how to do it: [writebots_website](https://www.writebots.com/discord-bot-token/) or [youtube_video](https://www.youtube.com/watch?v=SPTfmiYiuok)

OR you can use Docker to run the bot by following the instructions below :

1. Installing Docker : [docker_website](https://docs.docker.com/get-docker/)
2. Clone this repository
3. Run the Dockerfile with `docker build --build-arg token=<your_token> --build-arg channel_id=<your_channel_id> -t self-improvement-bot`.
4. Run the Dockerfile with `docker run -d self-improvement-bot`
5. Enjoy !

# Logs Storage

The bot will create a folder named `logs` in the folder where the bot is located.
It will store all the logs (with commands that have been used) in a file named with the format `YYYY-MM-DD-DiscordIDServer.log` in the folder `logs`.
For example, the file `2021-01-01-123456789012345678.log` will contain all the logs of the server with the ID `123456789012345678` on the 1st of January 2021.

# Cooldown 

The bot has a cooldown of **10 seconds** for each command.
That means that you can't use the same command twice in less than 10 seconds.
It can be changed in the file `main.py` in the variable `COOLDOWN` in the function `on_command`.

# Quotes

The bot will send a random quote from Andrew Tate and other inspirationnal people to keep you motivated and help you to improve yourself.
The quotes are stored in the file `quotes.json` in the folder `data`.
You can add your own quotes in the file `quotes.json` in the folder `data` by following the same format as the other quotes.

# Commands.
- `!get_started` to get all the commands available.
- `!pushups ‹value>` add pushups to your total.
- `!pullups ‹value>` add pullups to your total.
- `!squats ‹value>` add squats to to your total.
- `!situps ‹value>` add situps to to your total.
- `!score` to get the user's total score and individual scores for each exercises.
- `!quote` to get a random quote with a GIF of Andrew Tate and more embedded into it.
- `!leaderboard` to get the leaderboard of the server.
- `!avatar` to get the user's avatar.
- `!topG` to get the server's topG of the month.

# Admin commands only.
- `!help_admin` to get all the admin commands available.
- `!reset_points ‹username>` to reset the user's total score and individual scores for each exercises.
- `!add_points ‹username> ‹points_for_pushups> ‹points_for_pullups> ‹points_for_squats> ` to add points to the user's total score and individual scores for each exercises.
- `!remove_points ‹username> ‹malus_for_pushups> ‹malus_for_pullups> ‹malus_for_squats> ` to remove points to the user's total score and individual scores for each exercises.
- `!reset_leaderboard` to reset the leaderboard.

More features and commands will be added soon.