import os
from settings import *
from process.fingerprint import generate_fingerprint


def store_one(name, fingerprints):
    # fingerprints
    fingerprints_docs = [{"hash": h[0], "offset": h[1]} for h in fingerprints]

    # Document for each fingerprints
    song_doc = {"name": name, "fingerprints": fingerprints_docs}

    # Insert the document into collection
    result = song_collection.insert_one(song_doc)

    # Result
    print(f"Inserted {name} with id: {result.inserted_id}")


def store_samples(samples_path):
    # Correct path
    if samples_path[len(samples_path) - 1] != '/':
        samples_path += '/'

    # Store all the samples into collection, skip
    for sample_name in os.listdir(samples_path):
        if song_collection.count_documents({"name": sample_name}) > 0:
            print("Skip", sample_name)
        else:
            store_one(sample_name, generate_fingerprint(samples_path + sample_name))

