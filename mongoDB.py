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
    tlsCAFile=certifi.where()
)

db = client["userdata"]
print(db.list_collection_names())