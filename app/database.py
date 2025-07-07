from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    database = None

# Database configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://admin:password123@localhost:27017/fastapi_db?authSource=admin")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fastapi_db")

# Collection names
ITEMS_COLLECTION = "items"
USERS_COLLECTION = "users"
LOGS_COLLECTION = "logs"

async def connect_to_mongo():
    """Create database connection"""
    try:
        Database.client = AsyncIOMotorClient(MONGODB_URL)
        Database.database = Database.client[DATABASE_NAME]
        
        # Test the connection
        await Database.client.admin.command('ping')
        logger.info("Successfully connected to MongoDB!")
        
        # Create indexes for better performance
        await create_indexes()
        
    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise e

async def close_mongo_connection():
    """Close database connection"""
    if Database.client:
        Database.client.close()
        logger.info("Disconnected from MongoDB")

async def create_indexes():
    """Create database indexes for better performance"""
    try:
        # Items collection indexes
        items_collection = Database.database[ITEMS_COLLECTION]
        await items_collection.create_index("name")
        await items_collection.create_index("category")
        await items_collection.create_index("price")
        await items_collection.create_index("tags")
        await items_collection.create_index([("name", "text"), ("description", "text")])
        
        # Users collection indexes
        users_collection = Database.database[USERS_COLLECTION]
        await users_collection.create_index("username", unique=True)
        await users_collection.create_index("email", unique=True)
        
        logger.info("Database indexes created successfully")
        
    except Exception as e:
        logger.error(f"Error creating indexes: {e}")

def get_database():
    """Get database instance"""
    return Database.database

def get_collection(collection_name: str):
    """Get specific collection"""
    return Database.database[collection_name]