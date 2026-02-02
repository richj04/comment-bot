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

print("database is on!")

def checkUserExist( userID ):
    user = user_prompts.find_one({"userid": userID})
    if user:
        return True
    return False
    
def createUser( userID, userPrompt ):
    user_prompts.insert_one({
        "userid": userID,
        "prompt": userPrompt,
        "tokens": 8
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
    user_prompts.update_one(
        {"userid: userID"},
        {"$inc": {"tokens": -1}}
    )












