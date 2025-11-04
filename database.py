from pymongo import MongoClient
from dotenv import load_dotenv
import os
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError


# Load env variable from .env file
# load_dotenv()

# MONGO_URL = os.getenv("MONGO_URL")
# DB_NAME   = os.getenv("DB_NAME")

# Create Mongo client and reference to database
try:
    client = MongoClient(os.getenv("MONGODB_URI"), serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    print(f"Connected to MongoDB at {os.getenv('MONGODB_URI')}")
    db = client["haasapp"]
except ConnectionFailure as e:
    print(f"Could not connect to MongoDB: {e}")
    db = None

