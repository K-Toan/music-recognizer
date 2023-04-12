from database.config import *
from collections import defaultdict


def get_matches(hashes, threshold=5):
    h_dict = {}
    for h, t, _ in hashes:
        h_dict[h] = t
    in_values = f"({','.join([str(h[0]) for h in hashes])})"

    # Tạo danh sách giá trị hash để truy vấn trong cơ sở dữ liệu
    hash_values = [str(h[0]) for h in hashes]

    # Tìm kiếm các bản ghi trong cơ sở dữ liệu MongoDB
    results = song_collection.find({"hash": {"$in": hash_values}})

    # Lấy kết quả của các bản ghi tìm thấy
    result_list = [(r["hash"], r["offset"], r["song_id"]) for r in results]

    result_dict = defaultdict(list)
    for r in result_list:
        result_dict[r[2]].append((r[1], h_dict[r[0]]))
    return result_dict


def get_matches_list(hashes):
    h_dict = {}
    # h ~ hash: int
    # t ~ time offset: real
    for h, t, _ in hashes:
        h_dict[h] = t

    result_dict = defaultdict(list)
    for sample in song_collection.find():
        sample_h_dict = {}
        for h, t, _ in sample["fingerprints"]:
            sample_h_dict[h] = t

        # Find matching hashes between the two audio files
        matched_hashes = set(h_dict.keys()) & set(sample_h_dict.keys())
        result_dict[sample["name"]].append(("scores", len(matched_hashes)))
    return result_dict


def get_best_match(hashes):
    h_dict = {}
    for h, t, _ in hashes:
        h_dict[h] = t

    matched_song = None
    best_score = -1

    for sample in song_collection.find():
        sample_h_dict = {}
        for h, t, _ in sample["fingerprints"]:
            sample_h_dict[h] = t

        # Find matching hashes between the two fingerprints
        score = len(set(h_dict.keys()) & set(sample_h_dict.keys()))

        # Update best match
        if best_score < score:
            best_score = score
            matched_song = sample["name"]

    return matched_song

