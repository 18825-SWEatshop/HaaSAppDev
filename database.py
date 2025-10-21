import pymongo
from dotenv import load_dotenv
import os
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError


# Load env variable from .env file
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME   = os.getenv("DB_NAME")

# Create Mongo client and reference to database
try:
    client = pymongo.MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    print(f"Connected to MongoDB at {MONGO_URL}")
    db = client[DB_NAME]
except ConnectionFailure as e:
    print(f"Could not connect to MongoDB: {e}")
    db = None

