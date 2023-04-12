import numpy as np
from process import fingerprint
from database.fetch import *


def score_match(offsets):
    # Use bins spaced 0.5 seconds apart
    binwidth = 0.5
    tks = list(map(lambda x: x[0] - x[1], offsets))
    hist, _ = np.histogram(tks,
                           bins=np.arange(int(min(tks)),
                                          int(max(tks)) + binwidth + 1,
                                          binwidth))
    return np.max(hist)


def recognize_song(filepath):
    hashes = fingerprint.generate_fingerprint(filepath)
    matched_song = get_best_match(hashes)
    print(matched_song)

    matches_list = get_matches_list(hashes)
    # for song in matches_list.items():
    #     print(song)




























# def get_matches_from_files(audio_file1, audio_file2, threshold=5):
#     # Generate hashes for both audio files
#     hashes1 = fingerprint.generate_fingerprint(audio_file1)
#     hashes2 = fingerprint.generate_fingerprint(audio_file2)
#
#     # Build dictionaries of hashes for both audio files
#     h_dict1 = {}
#     h_dict2 = {}
#     for h, t, _ in hashes1:
#         h_dict1[h] = t
#     for h, t, _ in hashes2:
#         h_dict2[h] = t
#
#     # Find matching hashes between the two audio files
#     matched_hashes = set(h_dict1.keys()) & set(h_dict2.keys())
#
#     # Build result dictionary
#     result_dict = defaultdict(list)
#     for h in matched_hashes:
#         for r1 in [r for r in hashes1 if r[0] == h]:
#             for r2 in [r for r in hashes2 if r[0] == h]:
#                 result_dict[r1[2]].append((r2[1], r1[1]))
#
#     # Return song matches with a score greater than the threshold
#     return {song_id: offsets for song_id, offsets in result_dict.items() if len(offsets) >= threshold}
