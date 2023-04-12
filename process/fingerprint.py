import uuid
import numpy as np
from process import config
from pydub import AudioSegment
from scipy.signal import spectrogram
from scipy.ndimage import maximum_filter


def file_to_spectrogram(filename):
    """Calculates the spectrogram of a file."""
    a = AudioSegment.from_file(filename).set_channels(1).set_frame_rate(config.SAMPLE_RATE)
    audio = np.frombuffer(a.raw_data, np.int16)
    nperseg = int(config.SAMPLE_RATE * config.FFT_WINDOW_SIZE)
    return spectrogram(audio, config.SAMPLE_RATE, nperseg=nperseg)


def find_peaks(Sxx):
    """Finds peaks in a spectrogram."""
    data_max = maximum_filter(Sxx, size=config.PEAK_BOX_SIZE, mode='constant', cval=0.0)
    peak_goodmask = (Sxx == data_max)  # good pixels are True
    y_peaks, x_peaks = peak_goodmask.nonzero()
    peak_values = Sxx[y_peaks, x_peaks]
    i = peak_values.argsort()[::-1]
    # get co-ordinates into arr
    j = [(y_peaks[idx], x_peaks[idx]) for idx in i]
    total = Sxx.shape[0] * Sxx.shape[1]
    # in a square with a perfectly spaced grid, we could fit area / PEAK_BOX_SIZE^2 points
    # use point efficiency to reduce this, since it won't be perfectly spaced
    # accuracy vs speed tradeoff
    peak_target = int((total / (config.PEAK_BOX_SIZE**2)) * config.POINT_EFFICIENCY)
    return j[:peak_target]


def idxs_to_tf_pairs(idxs, t, f):
    """Helper function to convert time/frequency indices into values."""
    return np.array([(f[i[0]], t[i[1]]) for i in idxs])


def hash_point_pair(p1, p2):
    """Helper function to generate a hash from two time/frequency points."""
    return hash((p1[0], p2[0], p2[1]-p2[1]))


def target_zone(anchor, points, width, height, t):
    """Generates a target zone as described in the Shazam paper"""
    x_min = anchor[1] + t
    x_max = x_min + width
    y_min = anchor[0] - (height*0.5)
    y_max = y_min + height
    for point in points:
        if point[0] < y_min or point[0] > y_max:
            continue
        if point[1] < x_min or point[1] > x_max:
            continue
        yield point


def hash_points(points, file_path):
    """Generates all hashes for a list of peaks."""
    hashes = []
    song_id = uuid.uuid5(uuid.NAMESPACE_OID, file_path).int
    for anchor in points:
        for target in target_zone(
            anchor, points, config.TARGET_T, config.TARGET_F, config.TARGET_START
        ):
            hashes.append((
                # hash
                hash_point_pair(anchor, target),
                # time offset
                anchor[1],
                # filename
                str(song_id)
            ))
    return hashes


def generate_fingerprint(file_path):
    """Generate hashes for a file."""
    f, t, Sxx = file_to_spectrogram(file_path)
    peaks = find_peaks(Sxx)
    peaks = idxs_to_tf_pairs(peaks, t, f)
    return hash_points(peaks, file_path)

