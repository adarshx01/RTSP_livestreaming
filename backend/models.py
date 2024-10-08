# backend/models.py

from pymongo import MongoClient
import os

# Get MongoDB URI from environment variables
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/streaming_app')

client = MongoClient(MONGO_URI)
db = client.streaming_app
overlays_collection = db.overlays
