import os
import glob
import numpy as np
from settings import *
from process.fingerprint import generate_fingerprint
from database.fetch import get_matches


def score_match(offsets):
    """Score a matched song.
    :param offsets: List of offset pairs for matching hashes
    :returns: The highest peak in a histogram of time deltas
    :rtype: int
    """
    bin_width = BIN_WIDTH
    tks = list(map(lambda x: x[0] - x[1], offsets))
    hist, _ = np.histogram(tks,
                           bins=np.arange(int(min(tks)),
                                          int(max(tks)) + bin_width + 1,
                                          bin_width))
    return np.max(hist)


def best_match(matches):
    """For a dictionary of song_id: offsets, returns the best song_id.
    Scores each song in the matches dictionary and then returns the song_id with the best score.
    :param matches: Dictionary of song_id to list of offset pairs (db_offset, sample_offset)
       as returned by :func:`~fetch.get_matches`.
    :returns: song_name with the best score.
    :rtype: str
    """
    matched_song = None
    best_score = 0
    for song_name, offsets in matches.items():
        if len(offsets) < best_score:
            # can't be best score, avoid expensive histogram
            continue
        score = score_match(offsets)
        print(f"{song_name} - {score}")
        if score > best_score:
            best_score = score
            matched_song = song_name
    print(f"---------------Matched song: {matched_song}---------------")
    return matched_song


def recognize_song(file_path):
    """Recognises a pre-recorded sample."""
    fingerprints = generate_fingerprint(file_path)
    matches = get_matches(fingerprints)
    matched_song = best_match(matches)
    return matched_song


def recognize_multiple_songs(dir_path):
    for file_path in glob.glob(os.path.join(dir_path, '*')):
        if os.path.isfile(file_path):
            recognize_song(dir_path + os.path.basename(file_path))
