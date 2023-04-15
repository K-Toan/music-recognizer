from settings import *
from collections import defaultdict


def get_matches(fingerprints):
    """Get matching songs for a set of hashes.
    :param fingerprints: A list of hashes as returned by
        :func:`~fingerprint.generate_fingerprints`.
    :returns: A dictionary mapping ``song_name`` to a list of time offset tuples. The tuples are of
        the form (result offset, original hash offset).
    :rtype: dict(str: list(tuple(float, float)))
    """
    # query hashes
    query_h_dict = {}
    for h, t in fingerprints:
        query_h_dict[h] = t

    # song list
    sample_docs = song_collection.find()

    # dictionary contains song_name : fingerprints
    result_dict = defaultdict(list)

    # each song
    for sample in sample_docs:
        # sample hashes
        sample_h_dict = {}

        # generate sample hashes
        for fingerprints in sample["fingerprints"]:
            sample_h_dict[fingerprints["hash"]] = fingerprints["offset"]

        # Find matching hashes between the two audio files
        matched_hashes = set(query_h_dict.keys()) & set(sample_h_dict.keys())
        for h in matched_hashes:
            result_dict[sample["name"]].append((query_h_dict[h], sample_h_dict[h]))

    return result_dict
