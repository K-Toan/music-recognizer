import os
from database.config import *
from process.fingerprint import generate_fingerprint


# Store fingerprints into database
def store_one(name, fingerprints):
    # Document for each fingerprints
    fingerprint_document = {"name": name, "fingerprints": fingerprints}

    # Insert the document into collection
    result = song_collection.insert_one(fingerprint_document)

    # Result
    print(f"Inserted {name} with id: {result.inserted_id}")


def store_samples(samples_path, display=False):
    # Correct path
    if samples_path[len(samples_path) - 1] != '/':
        samples_path += '/'

    # Clear and store all samples fingerprint into database
    print(f"Deleted rows count:", song_collection.delete_many({}).deleted_count)

    # Store all the samples into collection
    for sample_name in os.listdir(samples_path):
        sample_fingerprint = generate_fingerprint(samples_path + sample_name)
        store_one(sample_name, sample_fingerprint)

    # Display all samples in the collection
    if display:
        for sample in db.song_collection.find():
            print(sample)
