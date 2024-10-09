import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

# MongoDB credentials
password = "bd25whIbLwZ8s0cu"
mongo_uri = f"mongodb+srv://mukomampashi2:{password}@cluster0.p3kqxqy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a MongoDB client using Motor for async operations
mongo_client = AsyncIOMotorClient(mongo_uri, server_api=ServerApi('1'))

# Define the database and collection names
db_name = 'smart_greenhouse'
collections = ['sensor_data', 'irrigation_settings', 'temperature_settings', 'device_status', 'logs']

# Function to set up collections in the MongoDB database
async def setup_mongodb():
    db = mongo_client[db_name]  # Select the database
    
    # Iterate through the collection names and create each one
    for collection_name in collections:
        collection = db[collection_name]
        await collection.create_index("timestamp")  # Optional: Indexing timestamp for faster queries
        print(f"Collection '{collection_name}' created and indexed.")
    
    print("MongoDB setup completed.")

# Run the setup
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup_mongodb())
