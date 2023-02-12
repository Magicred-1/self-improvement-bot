# self-improvement-bot
## Andrew Tate's self-improvement bot
**By: [Djason Gadiou](https://github.com/Magicred-1/)**

This is a simple bot that will help you to improve yourself. It will send you a message every day with a new task to do. You can also add your own tasks.

## How to use it

1. Clone this repository
2. Rename the file `.env.example` to `.env`
3. Add your discord bot token in the `.env` file and the channel id where you want the bot to send the messages.
4. Run `py -3 main.py` in the terminal from folder where the bot is located.

# Commands
`!get_started` to get all the commands available.
`!pushups ‹value>` add pushups to the user's total.
`!pullups ‹value>` add pullups to the user's total.
`!squats ‹value>` add squats to the user's total.
`!situps ‹value>` add situps to the user's total.
`!score` to get the user's total score and individual scores for each exercises.
`!quote` to get a random quote.

# Admin commands
`!reset_points ‹username>` to reset the user's total score and individual scores for each exercises.
`!add_points ‹username> ‹points_for_pushups> ‹points_for_pullups> ‹squats> ` to add points to the user's total score and individual scores for each exercises.
WIP: `!reset_leaderboard` to reset the leaderboard.