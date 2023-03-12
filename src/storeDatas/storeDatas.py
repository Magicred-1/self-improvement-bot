import json
import os
import datetime # For the logs
from dotenv import load_dotenv # For the .env file

EXERCISES = ["pushups", "pullups", "squats", "jumping_jacks", "burpees", "situps"]

FILE_SOURCE = "./leaderboard.json"

# Discord stuff
# Loads the token and the channel id from the .env file
load_dotenv()

TOKEN = os.getenv("token")
CHANNEL = os.getenv("channel")
GUILD = os.getenv("guild")

COOLDOWN = 10  # Cooldown for the commands in seconds


def writeLogs(ctx, message):
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    date_time = datetime.datetime.now().strftime("%d-%m-%Y")
    date_hour = datetime.datetime.now().strftime("%H:%M:%S")
    discordServerID = ctx.guild.id

    if not os.path.exists("logs"):
        os.makedirs("logs")

    logs_file = open(f"./logs/{date}-{discordServerID}.logs", "a")
    logs_file.write(f'{date_time} {date_hour} : [LOGS] {message}\n')
    print(f'{date_time} {date_hour} : [LOGS] {message}')
    logs_file.close()

def initLeaderboard():
    # Create a new leaderboard file and create the Andrew Tate's Bot account
    if os.path.exists(FILE_SOURCE) == False:
        with open(FILE_SOURCE, "w") as f:
            json.dump({}, f)
    with open(FILE_SOURCE, "r") as f:
        leaderboard = json.load(f)
        if "1074307468160667648" not in leaderboard: # 1074307468160667648 is the user_id of the Andrew Tate's bot account
            leaderboard["1074307468160667648"] = {
                "_username": "Andrew Tate's bot account",
                "top_g_of_the_month": {
                    "user_id": 0,
                    "username": "",
                    "date": {
                        "day": 0,
                        "month": 0,
                        "year": 0,
                    },
                },
                "exercises": {
                    "pushups": 0,
                    "pullups": 0,
                    "squats": 0,
                    "jumping_jacks": 0,
                    "burpees": 0,
                    "situps": 0,
                },
            }
        
    with open(FILE_SOURCE, "w") as f:
        json.dump(leaderboard, f, indent=4)

def updateLeaderboard(username, exercise, value, user_id):
    with open("./leaderboard.json", "r") as f:
        leaderboard = json.load(f)
        if str(user_id) in leaderboard:
            if username != leaderboard[str(user_id)]["username"]: 
                leaderboard[str(user_id)]["username"] = username
            leaderboard[str(user_id)]["exercises"][exercise] += value
        else:
            leaderboard[str(user_id)] = {
                "username": username,
                "exercises": {
                    "pushups": 0,
                    "pullups": 0,
                    "squats": 0,
                    "jumping_jacks": 0,
                    "burpees": 0,
                    "situps": 0,
                },
            }
            leaderboard[str(user_id)]["exercises"][exercise] += value
    with open("./leaderboard.json", "w") as f:
        json.dump(leaderboard, f, indent=4)


def deleteUserLeaderboard(user_id):
    # Delete the user from the leaderboard
    with open("./leaderboard.json", "r") as f:
        leaderboard = json.load(f)
        if str(user_id) in leaderboard:
            del leaderboard[str(user_id)]
    with open("./leaderboard.json", "w") as f:
        json.dump(leaderboard, f, indent=4)

def getLeaderboard():
    # Get the leaderboard
    with open("./leaderboard.json", "r") as f:
        leaderboard = json.load(f)
    return leaderboard


def getUserScore(user_id):
    # Get the score of a user
    with open("./leaderboard.json", "r") as f:
        leaderboard = json.load(f)
        
        if str(user_id) in leaderboard and "exercises" in leaderboard[str(user_id)]:

            pushups = 0
            pullups = 0
            squats = 0
            jumping_jacks = 0
            burpees = 0
            situps = 0

            if "pushups" in leaderboard[str(user_id)]["exercises"]:
                pushups = leaderboard[str(user_id)]["exercises"]["pushups"]
            if "pullups" in leaderboard[str(user_id)]["exercises"]:
                pullups = leaderboard[str(user_id)]["exercises"]["pullups"]
            if "squats" in leaderboard[str(user_id)]["exercises"]:
                squats = leaderboard[str(user_id)]["exercises"]["squats"]
            if "jumping_jacks" in leaderboard[str(user_id)]["exercises"]:
                jumping_jacks = leaderboard[str(user_id)]["exercises"]["jumping_jacks"]
            if "burpees" in leaderboard[str(user_id)]["exercises"]:
                burpees = leaderboard[str(user_id)]["exercises"]["burpees"]
            if "situps" in leaderboard[str(user_id)]["exercises"]:
                situps = leaderboard[str(user_id)]["exercises"]["situps"]

            score = (
                pushups + 
                pullups * 2 
                + squats // 5 
                + jumping_jacks 
                // 3 + 
                burpees * 2 
                + situps // 2
            )

            return score


def getUsernameByUserID(user_id):
    # Get the username of a user by his user_id
    with open("./leaderboard.json", "r") as f:
        leaderboard = json.load(f)
        if str(user_id) in leaderboard:
            return leaderboard[str(user_id)]["username"]


def getTotalScore():
    # Get the total score of all users in the leaderboard except the Andrew Tate's bot account
    with open("./leaderboard.json", "r") as f:
        leaderboard = json.load(f)
        totalScore = 0
        for user_id in leaderboard:
            totalScore += getUserScore(str(user_id))
        else:
            totalScore += 0
    return totalScore


def getTheTopG():
    # get month name
    month = datetime.datetime.now().strftime("%B")

    with open("./leaderboard.json", "r") as f:
        leaderboard = json.load(f)
        if (
            "1074307468160667648" in leaderboard and leaderboard["1074307468160667648"]["top_g_of_the_month"]["username"] != ""
        ):
            topG = leaderboard["1074307468160667648"]["top_g_of_the_month"]["username"]
        else:
            topG = f"The TOP G of {month} is not set yet. \nYou can set it by using the command /settopg"
    return topG


def setTheTopG(ctx, user_id):
    # We set the TOP_G_OF_THE_MONTH and we update the date
    current_day = datetime.datetime.now().date().day
    current_month = datetime.datetime.now().date().month
    current_year = datetime.datetime.now().date().year
    full_date_plus_1 = f"{current_day}/{current_month+1}/{current_year}"

    user_id = str(user_id)

    # We get the username of the user_id

    username = ctx.guild.get_member(int(user_id)).name

    with open("./leaderboard.json", "r") as f:
        leaderboard = json.load(f)
        if "1074307468160667648" in leaderboard:
            if (
                leaderboard["1074307468160667648"]["top_g_of_the_month"]["date"]["day"] == current_day
                and leaderboard["1074307468160667648"]["top_g_of_the_month"]["date"]["month"] == current_month
                and leaderboard["1074307468160667648"]["top_g_of_the_month"]["date"]["year"] == current_year
            ):
                return False
            else:
                leaderboard["1074307468160667648"]["top_g_of_the_month"]["username"] = username
                leaderboard["1074307468160667648"]["top_g_of_the_month"]["date"]["day"] = current_day
                leaderboard["1074307468160667648"]["top_g_of_the_month"]["date"]["month"] = current_month
                leaderboard["1074307468160667648"]["top_g_of_the_month"]["date"]["year"] = current_year
        else:
            leaderboard["1074307468160667648"] = {
                "username": "Andrew Tate's bot account",
                "exercises": {
                    "pushups": 0,
                    "pullups": 0,
                    "squats": 0,
                    "jumping_jacks": 0,
                    "burpees": 0,
                    "situps": 0,
                },
                "top_g_of_the_month": {
                    "username": username,
                    "date": {
                        "day": current_day,
                        "month": current_month,
                        "year": current_year,
                    },
                },
            }
            return True  

    with open("./leaderboard.json", "w") as f:
        json.dump(leaderboard, f, indent=4)


initLeaderboard()