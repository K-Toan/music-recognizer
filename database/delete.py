from settings import *


def delete_by_id(song_id):
    # Delete song by song_id
    print(f"Deleted rows:", song_collection.delete_one({"_id": str(song_id)}).deleted_count)


def delete_by_name(name):
    # Delete song by song_name
    print(f"Deleted rows:", song_collection.delete_one({"name": str(name)}).deleted_count)


def delete_all():
    # Remove all samples fingerprint into database
    print(f"Deleted rows count:", song_collection.delete_many({}).deleted_count)
