import uuid
import numpy as np
from settings import *
from pydub import AudioSegment
from scipy.signal import spectrogram
from scipy.ndimage import maximum_filter


def my_spectrogram(audio):
    """Helper function that performs a spectrogram with the values in settings."""
    nperseg = int(SAMPLE_RATE * FFT_WINDOW_SIZE)
    return spectrogram(audio, SAMPLE_RATE, nperseg=nperseg)


def file_to_spectrogram(file_path):
    """Calculates the spectrogram of a file.
    :param file_path: Path to the file to spectrogram.
    :returns: * f - list of frequencies
              * t - list of times
              * Sxx - Power value for each time/frequency pair
    """
    a = AudioSegment.from_file(file_path).set_channels(1).set_frame_rate(SAMPLE_RATE)
    audio = np.frombuffer(a.raw_data, np.int16)
    return my_spectrogram(audio)


def find_peaks(Sxx):
    """Finds peaks in a spectrogram.
    :param Sxx: The spectrogram.
    :returns: A list of peaks in the spectrogram.
    """
    data_max = maximum_filter(Sxx, size=PEAK_BOX_SIZE, mode='constant', cval=0.0)
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
    peak_target = int((total / (PEAK_BOX_SIZE ** 2)) * POINT_EFFICIENCY)
    return j[:peak_target]


def idxs_to_tf_pairs(idxs, t, f):
    """Helper function to convert time/frequency indices into values."""
    return np.array([(f[i[0]], t[i[1]]) for i in idxs])


def hash_point_pair(p1, p2):
    """Helper function to generate a hash from two time/frequency points."""
    return hash((p1[0], p2[0], p2[1] - p2[1]))


def target_zone(anchor, points, width, height, t):
    """Generates a target zone as described in `the Shazam paper
    :param anchor: The anchor point
    :param points: The list of points to search
    :param width: The width of the target zone
    :param height: The height of the target zone
    :param t: How many seconds after the anchor point the target zone should start
    :returns: Yields all points within the target zone.
    """
    x_min = anchor[1] + t
    x_max = x_min + width
    y_min = anchor[0] - (height * 0.5)
    y_max = y_min + height
    for point in points:
        if point[0] < y_min or point[0] > y_max:
            continue
        if point[1] < x_min or point[1] > x_max:
            continue
        yield point


def hash_points(points):
    """Generates all hashes for a list of peaks.
    :param points: The list of peaks.
    :returns: A list of tuples of the form (hash, time offset, song_id).
    """
    hashes = []
    for anchor in points:
        for target in target_zone(anchor, points, TARGET_T, TARGET_F, TARGET_START):
            hashes.append((hash_point_pair(anchor, target),  # hash
                           anchor[1]))  # time offset
    return hashes


def generate_song_id(file_path):
    """Unused because mongoDB already generate _id"""
    return uuid.uuid5(uuid.NAMESPACE_OID, file_path).int


def generate_fingerprint(file_path):
    """Generate hashes for a file.
    :param file_path: The path to the file.
    :returns: The output of :func:`hash_points`.
    """
    print(f"\n---------------Hashing {os.path.basename(file_path)}---------------")
    f, t, Sxx = file_to_spectrogram(file_path)
    peaks = find_peaks(Sxx)
    peaks = idxs_to_tf_pairs(peaks, t, f)
    return hash_points(peaks)
