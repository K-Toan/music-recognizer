from pymongo import MongoClient


# Connection configuration
conn = MongoClient("mongodb://localhost:27017/")
db = conn["songs"]
song_collection = db["audio_fingerprints"]
