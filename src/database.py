"""
Database configuration and connection management for MongoDB.
"""

import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB connection string from environment or use default
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "mergington_high_school")

# MongoDB client
client = None
db = None


def connect_to_mongo():
    """Connect to MongoDB database."""
    global client, db
    try:
        client = MongoClient(MONGODB_URL)
        # Verify connection
        client.admin.command('ping')
        db = client[DATABASE_NAME]
        print(f"✓ Connected to MongoDB: {DATABASE_NAME}")
        return db
    except ConnectionFailure as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        raise


def close_mongo_connection():
    """Close MongoDB connection."""
    global client
    if client:
        client.close()
        print("✓ Closed MongoDB connection")


def get_database():
    """Get database instance."""
    if db is None:
        return connect_to_mongo()
    return db


def init_collections():
    """Initialize database collections with indexes."""
    database = get_database()
    
    # Create activities collection if it doesn't exist
    if "activities" not in database.list_collection_names():
        database.create_collection("activities")
        print("✓ Created 'activities' collection")
    
    # Create index on activity name
    database.activities.create_index("name", unique=True)
    
    # Create users collection if it doesn't exist
    if "users" not in database.list_collection_names():
        database.create_collection("users")
        print("✓ Created 'users' collection")
    
    # Create index on email
    database.users.create_index("email", unique=True)
    
    print("✓ Database initialization complete")
