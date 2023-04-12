import numpy as np
from process import fingerprint
from database import fetch


# def get_song_info(filename):
#     tag = TinyTag.get(filename)
#     artist = tag.artist if tag.albumartist is None else tag.albumartist
#     return (artist, tag.album, tag.title)


def score_match(offsets):
    # Use bins spaced 0.5 seconds apart
    binwidth = 0.5
    tks = list(map(lambda x: x[0] - x[1], offsets))
    hist, _ = np.histogram(tks,
                           bins=np.arange(int(min(tks)),
                                          int(max(tks)) + binwidth + 1,
                                          binwidth))
    return np.max(hist)


def best_match(matches):
    matched_song = None
    best_score = 0
    for song_id, offsets in matches.items():
        if len(offsets) < best_score:
            # can't be best score, avoid expensive histogram
            continue
        score = score_match(offsets)
        if score > best_score:
            best_score = score
            matched_song = song_id
    return matched_song


def recognise_song(filename):
    hashes = fingerprint.generate_fingerprint(filename)
    matches = fetch.get_matches(hashes)
    matched_song = best_match(matches)
    print(type(matched_song))
    print(matched_song)

    # info = get_info_for_song_id(matched_song)
    # if info is not None:
    #     return info
    # return matched_song
