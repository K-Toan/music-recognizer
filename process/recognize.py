import numpy as np
from settings import *
from process.fingerprint import generate_fingerprint
from database.fetch import get_matches


def register_song(file_path):
    pass


def register_directory(path):
    pass


def score_match(offsets):
    """Score a matched song."""
    # Use bins spaced 0.5 seconds apart
    binwidth = 0.5
    tks = list(map(lambda x: x[0] - x[1], offsets))
    hist, _ = np.histogram(tks,
                           bins=np.arange(int(min(tks)),
                                          int(max(tks)) + binwidth + 1,
                                          binwidth))
    return np.max(hist)


def best_match(matches):
    """For a dictionary of song_id: offsets, returns the best song_id."""
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
    return matched_song


def recognize_song(file_path):
    """Recognises a pre-recorded sample."""
    fingerprints = generate_fingerprint(file_path)
    matches = get_matches(fingerprints)
    matched_song = best_match(matches)
    print(f"---------------Matched song: {matched_song}---------------")
    return matched_song
