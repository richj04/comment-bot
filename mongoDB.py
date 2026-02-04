from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
import certifi

load_dotenv()  # Load .env file
URI = os.getenv('URI')
uri = f'{URI}'

client = MongoClient(
    uri,
    tls=True,
    tlsAllowInvalidCertificates=True
    #tlsCAFile=certifi.where()
)
db = client["userdata"]
user_prompts = db["user_prompts"]
selected_user = db["selected_user"]
print("database is on!")

def selectUser( guildID, userID):
    selected_user.update_one(
        {"guildid": guildID},
        {"$set":{"selecteduserid": userID}},
        upsert=True
    )

def getSelectedUser ( guildID ):
    guild = selected_user.find_one({"guildid":guildID})
    if guild is None:
        return None
    return guild.get("selecteduserid")


def checkUserExist( userID ):
    user = user_prompts.find_one({"userid": userID})
    if user:
        return True
    return False

def getPrompt (userID):
    user = user_prompts.find_one({"userid": userID})
    return user["prompt"]
    
def createUser( userID, userPrompt, userName ):
    user_prompts.insert_one({
        "userid": userID,
        "prompt": userPrompt,
        "tokens": 8,
        "username": userName
    })

def updateUserPrompt ( userID, userPrompt ):
    user_prompts.update_one(
        {"userid": userID},
        {"$set": {"prompt": userPrompt}}
        
    )

def checkValidTokens ( userID ):
    doc = user_prompts.find_one({"userid": userID})
    tokens = doc["tokens"]
    if tokens > 0:
        return True
    return False

def useToken ( userID ):
    result = user_prompts.update_one(
        {"userid": userID},
        {"$inc": {"tokens": -1}}
    )
    print(
        "useToken -> userid:", userID,
        "matched:", result.matched_count,
        "modified:", result.modified_count
    )












