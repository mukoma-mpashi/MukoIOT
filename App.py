from flask import Flask, jsonify, request
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from bson.json_util import dumps
from datetime import datetime

# MongoDB credentials
password = "bd25whIbLwZ8s0cu"
mongo_uri = f"mongodb+srv://mukomampashi2:{password}@cluster0.p3kqxqy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo_client = AsyncIOMotorClient(mongo_uri, server_api=ServerApi('1'))

# Initialize Flask app
app = Flask(__name__)

# Database and collections setup
db_name = 'smart_greenhouse'
db = mongo_client[db_name]

# Collections
sensor_data_collection = db['sensor_data']
irrigation_settings_collection = db['irrigation_settings']
temperature_settings_collection = db['temperature_settings']
device_status_collection = db['device_status']
logs_collection = db['logs']

# Utility function to log events
async def log_event(event_type, data):
    event = {
        "event": event_type,
        "data": data,
        "timestamp": datetime.utcnow()
    }
    await logs_collection.insert_one(event)

# Route to insert sensor data
@app.route('/sensor-data', methods=['POST'])
async def store_sensor_data():
    data = request.json
    data['timestamp'] = datetime.utcnow()
    await sensor_data_collection.insert_one(data)
    await log_event("Sensor Data Added", data)
    return jsonify({"status": "Sensor data saved"}), 201

# Route to retrieve all sensor data
@app.route('/sensor-data', methods=['GET'])
async def get_sensor_data():
    sensor_data = await sensor_data_collection.find().to_list(length=100)
    return dumps(sensor_data), 200

# Route to update irrigation settings
@app.route('/settings/irrigation', methods=['POST'])
async def update_irrigation_settings():
    settings_data = request.json
    await irrigation_settings_collection.update_one(
        {"setting": "moisture_threshold"},
        {"$set": {"value": settings_data['moisture_threshold'], "timestamp": datetime.utcnow()}},
        upsert=True
    )
    await log_event("Irrigation Settings Updated", settings_data)
    return jsonify({"status": "Irrigation settings updated"}), 200

# Route to update temperature settings
@app.route('/settings/temperature', methods=['POST'])
async def update_temperature_settings():
    settings_data = request.json
    await temperature_settings_collection.update_one(
        {"setting": "temp_range"},
        {"$set": {"min": settings_data['min_temp'], "max": settings_data['max_temp'], "timestamp": datetime.utcnow()}},
        upsert=True
    )
    await log_event("Temperature Settings Updated", settings_data)
    return jsonify({"status": "Temperature settings updated"}), 200

# Route to update device status
@app.route('/devices/status', methods=['POST'])
async def update_device_status():
    device_data = request.json
    await device_status_collection.update_one(
        {"device_id": device_data['device_id']},
        {"$set": {"status": device_data['status'], "timestamp": datetime.utcnow()}},
        upsert=True
    )
    await log_event("Device Status Updated", device_data)
    return jsonify({"status": "Device status updated"}), 200

# Route to retrieve logs
@app.route('/logs', methods=['GET'])
async def get_logs():
    logs = await logs_collection.find().to_list(length=100)
    return dumps(logs), 200

# Function to run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
