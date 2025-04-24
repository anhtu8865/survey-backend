import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()
# MongoDB connection details
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")  # Replace with your database name

# Initialize MongoDB client
client = AsyncIOMotorClient(MONGODB_URI)
db = client[DATABASE_NAME]

async def get_db():
    try:
        yield db
    finally:
        pass