import pymongo
from dotenv import load_dotenv
import os


# Load env variable from .env file
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

# Create Mongo client and reference to database
client = pymongo.MongoClient(MONGO_URL)
db = client[DB_NAME]
