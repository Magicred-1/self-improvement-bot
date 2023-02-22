import os
import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId

# Discord stuff
# Loads the token and the channel id and M from the .env file
load_dotenv()

MONGO_URI = os.getenv("mongo_uri")
TOKEN = os.getenv("token")
CHANNEL = os.getenv("channel")

client = MongoClient(MONGO_URI)
db = client["leaderboard"]
members = db["members"]

EXCLUDED_USERS = ["Admin", "TOP_G_OF_MONTH"]

EXERCISES = ["pushups", "pullups", "squats"]

# Working
def initLeaderboard():
    # Create a members Admin and TOP_G_OF_MONTH document into MongoDB
    if members.count_documents({}) == 0:
        members.insert_one(
            {
                "special_members": {
                    "Admin": {
                        "_id": ObjectId(),
                        "pushups": 0,
                        "pullups": 0,
                        "squats": 0,
                        "last_update": datetime.datetime.now(),
                    },
                    "TOP_G_OF_MONTH": {
                        "_id": ObjectId(),
                        "username": "Admin",
                        "last_update": datetime.datetime.now(),
                    }
                },
            },
        )
        members.insert_one(
            {
                "discord_members": {},
            },
        )

# Working
def initUserScore(username, user_id):
    if username not in EXCLUDED_USERS:
        # find the existing discord_members document
        discord_members_doc = members.find_one({"discord_members": {"$exists": True}})
        if discord_members_doc is None:
            # if the discord_members document does not exist, create a new one
            discord_members.insert_one({
                "discord_members": {
                    username: {
                        "_id": ObjectId(),
                        "discord_id": user_id,
                        "pushups": 0,
                        "pullups": 0,
                        "squats": 0,
                        "last_update": datetime.datetime.now(),
                    }
                }
            })
        else:
            # if the discord_members document exists, add the new user object to it
            discord_members = discord_members_doc["discord_members"]
            discord_members[username] = {
                "_id": ObjectId(),
                "discord_id": user_id,
            }
            # add fields from the EXERCISES array to the new user object
            for exercise in EXERCISES:
                discord_members[username][exercise.lower()] = 0
            members.update_one(
                {"discord_members": {"$exists": True}},
                {"$set": {"discord_members": discord_members}}
            )
            members.update_one(
                {"discord_members." + username: {"$exists": True}},
                {"$set": {"discord_members." + username + ".last_update": datetime.datetime.now()}}
            )

# Working
def updateLeaderboard(username, user_id, exercise, value):
    # Update the username in the discord_members db if the exercise was done before the last update
    if username not in EXCLUDED_USERS:
        discord_members_doc = members.find_one({"discord_members": {"$exists": True}})
        if discord_members_doc is not None:
            discord_members = discord_members_doc["discord_members"]
            if username in discord_members:
                if discord_members[username]["last_update"] < datetime.datetime.now():
                    discord_members[username][exercise] += value
                    discord_members[username]["last_update"] = datetime.datetime.now()
                    members.update_one(
                        {"discord_members": {"$exists": True}},
                        {"$set": {"discord_members": discord_members}}
                    )
                    return True
                else:
                    return False
            else:
                initUserScore(username, user_id)
                updateLeaderboard(username, user_id, exercise, value)

# Working
def deleteUserLeaderboard(username):
    # Delete a user from the members db
    if username not in EXCLUDED_USERS:
        discord_members_doc = members.find_one({"discord_members": {"$exists": True}})
        if discord_members_doc is not None:
            discord_members = discord_members_doc["discord_members"]
            if username in discord_members:
                members.update_one(
                    {"discord_members": {"$exists": True}},
                    {"$unset": {"discord_members." + username: ""}}
                )
                return True
        else:
            return False


# # In progress
# def getLeaderboard():
#     # Retrieve all documents (i.e. members) from the leaderboard.discord_members collection
#     leaderboard = []
#     for member in members.find({}):
#         user_data = member["discord_members"]
#         for user in user_data:
#             leaderboard.append({
#                 "username": user,
#                 "pushups": user_data[user]["pushups"],
#                 "pullups": user_data[user]["pullups"],
#                 "squats": user_data[user]["squats"],
#             })

#     return leaderboard


def getUserScore(username):
    # Get the total score of a user in the discord_members db (sum of all the exercises)
    if username not in EXCLUDED_USERS:
        user_score = 0
        for exercise in EXERCISES:
            user_score += members.find_one({"discord_members": {}})["discord_members"][username][exercise]
        return user_score


def getTotalScore():
    # Get the all the points of all the users in the discord_members db
    total_score = 0
    for user in members.find_one({"discord_members": {}})["discord_members"][user]:
        total_score += getUserScore(user)
    return total_score


def getTheTopG():
    # Get the username of the TOP_G_OF_THE_MONTH in special_members db
    top_g = members.find_one(sort=[("special_members.TOP_G_OF_MONTH", -1)])["special_members"]["TOP_G_OF_MONTH"]["username"]
    return top_g


def setTheTopG(username):
    # Get the current month as a string in format "MM"
    current_month = datetime.datetime.now().strftime("%m")

    # Get the current month as a string in format "MM" of the last TOP_G_OF_THE_MONTH
    last_month = members.find_one({"special_members.TOP_G_OF_MONTH": {"$exists": True}})["special_members"]["TOP_G_OF_MONTH"]["last_update"].strftime("%m")

    # If the current month is different from the last month, update the TOP_G_OF_THE_MONTH
    if current_month != last_month:
        members.update_one(
            {"special_members.TOP_G_OF_MONTH": {"$exists": True}},
            {
                "$set": {
                    "special_members.TOP_G_OF_MONTH.username": username,
                    "special_members.TOP_G_OF_MONTH.last_update": datetime.datetime.now(),
                }
            },
        )
        return True
    else:
        return False


initLeaderboard()
