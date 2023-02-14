import json
import os
import datetime
import calendar as cal

def initLeaderboard():
    # Create a new leaderboard file
    if not os.path.exists('leaderboard.json') and os.path.getsize('leaderboard.json') == 0:    
        leaderboard = {}
        with open('leaderboard.json', 'w') as f:
            json.dump(leaderboard, f, indent=4)
    else:
        return

def updateLeaderboard(username, exercise, value):
    # Update the leaderboard with the new value
    with open('leaderboard.json', 'r') as f:
        leaderboard = json.load(f)
        if username in leaderboard:
            if exercise in leaderboard[username]:
                leaderboard[username][exercise] += value
            else:
                leaderboard[username][exercise] = value
        else:
            leaderboard[username] = {exercise: value}
    with open('leaderboard.json', 'w') as f:
        json.dump(leaderboard, f, indent=4)

def deleteUserLeaderboard(username):
    # Delete the user from the leaderboard
    with open('leaderboard.json', 'r') as f:
        leaderboard = json.load(f)
        if username in leaderboard:
            del leaderboard[username]
    with open('leaderboard.json', 'w') as f:
        json.dump(leaderboard, f, indent=4)

def getLeaderboard():
    # Get the leaderboard
    with open('leaderboard.json', 'r') as f:
        leaderboard = json.load(f)
    return leaderboard

def getUserScore(username):
    # Get the score of a user
    with open('leaderboard.json', 'r') as f:
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

def getCumuledScore(user):
    # Get the cumuled score of all users in the leaderboard
    with open('leaderboard.json', 'r') as f:
        leaderboard = json.load(f)
        cumuledScore = 0
        #pushups count for 1 point / Pullups count for 2 points / Squats count for 1 per 5 squats
        for user in leaderboard:
            if "pushups" in leaderboard[user] != 0:
                cumuledScore += leaderboard[user]["pushups"]
            if "pullups" in leaderboard[user] != 0:
                cumuledScore += leaderboard[user]["pullups"] * 2
            if "squats" in leaderboard[user] != 0:
                cumuledScore += leaderboard[user]["squats"] // 5
        else:
            cumuledScore += 0
    return cumuledScore

def getTotalScore():
    # Get the total score of all users in the leaderboard
    with open('leaderboard.json', 'r') as f:
        leaderboard = json.load(f)
        totalScore = 0
        for user in leaderboard:
            totalScore += getUserScore(user)
        else:
            totalScore += 0
    return totalScore

def getTheTopG():
    # Get the username of the TOP_G_OF_THE_MONTH
    with open('leaderboard.json', 'r') as f:
        leaderboard = json.load(f)
        if "TOP G OF MONTH" in leaderboard:
            topG = leaderboard["TOP G OF MONTH"]["username"]
        else:
            topG = "The TOP_G_OF_THE_MONTH is not set yet."
    return topG

def setTheTopG(username):
    current_day = datetime.datetime.now().date().day
    current_month = datetime.datetime.now().date().month
    current_year = datetime.datetime.now().date().year

    with open('leaderboard.json', 'r') as f:
        leaderboard = json.load(f)
        if "TOP G OF MONTH" in leaderboard:
            if current_month :
                leaderboard["TOP G OF MONTH"] = {"username": username, "date": {"day": current_day, "month": current_month, "year": current_year}}
            else:
                leaderboard["TOP G OF MONTH"]["username"] = username
                leaderboard["TOP G OF MONTH"]["date"]["day"] = current_day
                leaderboard["TOP G OF MONTH"]["date"]["month"] = current_month
                leaderboard["TOP G OF MONTH"]["date"]["year"] = current_year
        else:
            leaderboard["TOP G OF MONTH"] = {"username": username, "date": {"day": current_day, "month": current_month, "year": current_year}}
    with open('leaderboard.json', 'w') as f:
        json.dump(leaderboard, f, indent=4)

setTheTopG("Magicred1")

initLeaderboard()
