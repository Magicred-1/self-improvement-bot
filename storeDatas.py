import json
import os
import datetime

FILE_SOURCE = "./leaderboard.json"

def initLeaderboard():
    # Create a new leaderboard file and create the user TOP_G_OF_THE_MONTH & Admin user if the leaderboard file is empty
    if os.path.exists(FILE_SOURCE) == False:
        with open(FILE_SOURCE, "w") as f:
            json.dump({}, f)
    with open(FILE_SOURCE, "r") as f:
        leaderboard = json.load(f)
        if "TOP_G_OF_MONTH" not in leaderboard:
            leaderboard["TOP_G_OF_MONTH"] = {
                "username": "",
                "date": {"day": 0, "month": 0, "year": 0},
            }
        if "Admin" not in leaderboard:
            leaderboard["Admin"] = {"pushups": 0, "pullups": 0, "squats": 0}
    with open(FILE_SOURCE, "w") as f:
        json.dump(leaderboard, f, indent=4)


def initUserScore(username):
    # Create a new user in the leaderboard if the user is not in the leaderboard
    with open("./leaderboard.json", "r") as f:
        leaderboard = json.load(f)
        if username not in leaderboard:
            leaderboard[username] = {"pushups": 0, "pullups": 0, "squats": 0}
        else:
            if "pushups" not in leaderboard[username]:
                leaderboard[username]["pushups"] = 0
            if "pullups" not in leaderboard[username]:
                leaderboard[username]["pullups"] = 0
            if "squats" not in leaderboard[username]:
                leaderboard[username]["squats"] = 0
    with open("./leaderboard.json", "w") as f:
        json.dump(leaderboard, f, indent=4)


def updateLeaderboard(username, exercise, value):
# Update the leaderboard with the new value the rest of exercises will be 0

    initUserScore(username)

    with open("./leaderboard.json", "r") as f:
        leaderboard = json.load(f)

        if username in leaderboard:
            if exercise in leaderboard[username]:
                leaderboard[username][exercise] += value
            else:
                leaderboard[username][exercise] = value
        else:
            leaderboard[username] = {exercise: value}
    with open("./leaderboard.json", "w") as f:
        json.dump(leaderboard, f, indent=4)


def deleteUserLeaderboard(username):
    # Delete the user from the leaderboard
    with open("./leaderboard.json", "r") as f:
        leaderboard = json.load(f)
        if username in leaderboard:
            del leaderboard[username]
    with open("./leaderboard.json", "w") as f:
        json.dump(leaderboard, f, indent=4)


def getLeaderboard():
    # Get the leaderboard
    with open("./leaderboard.json", "r") as f:
        leaderboard = json.load(f)
    return leaderboard


def getUserScore(username):
    # Get the score of a user
    with open("./leaderboard.json", "r") as f:
        leaderboard = json.load(f)
        if username in leaderboard:
            pushups = 0
            pullups = 0
            squats = 0
            if "pushups" in leaderboard[username]:
                pushups = leaderboard[username]["pushups"]
            if "pullups" in leaderboard[username]:
                pullups = leaderboard[username]["pullups"]
            if "squats" in leaderboard[username]:
                squats = leaderboard[username]["squats"]
            return pushups + pullups * 2 + squats // 5
        else:
            return 0


def getTotalScore():
    # Get the total score of all users in the leaderboard
    with open("./leaderboard.json", "r") as f:
        leaderboard = json.load(f)
        totalScore = 0
        for user in leaderboard:
            totalScore += getUserScore(user)
        else:
            totalScore += 0
    return totalScore


def getTheTopG():
    # Get the username of the TOP_G_OF_THE_MONTH
    with open("./leaderboard.json", "r") as f:
        leaderboard = json.load(f)
        if (
            "TOP_G_OF_MONTH" in leaderboard
            and "username" in leaderboard["TOP_G_OF_MONTH"] == True
        ):
            topG = leaderboard["TOP_G_OF_MONTH"]["username"]
        else:
            topG = "The TOP_G_OF_THE_MONTH is not set yet."
    return topG


def setTheTopG(username):
    current_day = datetime.datetime.now().date().day
    current_month = datetime.datetime.now().date().month
    current_year = datetime.datetime.now().date().year

    with open("./leaderboard.json", "r") as f:
        leaderboard = json.load(f)
        if "TOP_G_OF_MONTH" in leaderboard:
            if current_month:
                leaderboard["TOP_G_OF_MONTH"] = {
                    "username": username,
                    "date": {
                        "day": current_day,
                        "month": current_month,
                        "year": current_year,
                    },
                }
            else:
                leaderboard["TOP_G_OF_MONTH"]["username"] = username
                leaderboard["TOP_G_OF_MONTH"]["date"]["day"] = current_day
                leaderboard["TOP_G_OF_MONTH"]["date"]["month"] = current_month
                leaderboard["TOP_G_OF_MONTH"]["date"]["year"] = current_year
        else:
            leaderboard["TOP_G_OF_MONTH"] = {
                "username": username,
                "date": {
                    "day": current_day,
                    "month": current_month,
                    "year": current_year,
                },
            }
    with open("./leaderboard.json", "w") as f:
        json.dump(leaderboard, f, indent=4)


initLeaderboard()