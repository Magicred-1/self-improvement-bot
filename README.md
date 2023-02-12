# self-improvement-bot
## Andrew Tate's self-improvement bot (Discord bot) using Python and Discord.py
**By: [Djason Gadiou](https://github.com/Magicred-1/)**

**Discord: Magicred1#3948**

This is a simple bot that will help you to improve yourself. It will send you a message every day with a new task to do. You can also add your own tasks.

## How to set up and use it ?

1. Clone this repository
2. Install the requirements with `pip install -r requirements.txt` with MacOS / Linux distro or `py -3 -m pip install -r requirements.txt` on Windows.
3. Rename the file `.env.example` to `.env`
4. Add your discord bot token in the `.env` file and the channel id where you want the bot to send the messages.
5. Run `py -3 main.py` in the terminal from folder where the bot is located.

# Commands.
- `!get_started` to get all the commands available.
- `!pushups ‹value>` add pushups to the user's total.
- `!pullups ‹value>` add pullups to the user's total.
- `!squats ‹value>` add squats to the user's total.
- `!situps ‹value>` add situps to the user's total.
- `!score` to get the user's total score and individual scores for each exercises.
- `!quote` to get a random quote with a GIF of Andrew Tate embedded into it.

# Admin commands only.
- `!help_admin` to get all the admin commands available.
- `!reset_points ‹username>` to reset the user's total score and individual scores for each exercises.
- `!add_points ‹username> ‹points_for_pushups> ‹points_for_pullups> ‹points_for_squats> ` to add points to the user's total score and individual scores for each exercises.
- `!remove_points ‹username> ‹malus_for_pushups> ‹malus_for_pullups> ‹malus_for_squats> ` to remove points to the user's total score and individual scores for each exercises.
- WIP: `!reset_leaderboard` to reset the leaderboard.

More features and commands will be added soon.