from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os


load_dotenv()
client = AsyncIOMotorClient(os.getenv("DB_URI"))
db = client.get_database("inventory_management")


def get_collection(collection):
    """creates a collection on db"""

    return db.get_collection(collection)
