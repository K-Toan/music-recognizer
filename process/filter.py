import numpy as np
import scipy.signal as signal
import scipy.io.wavfile as wavfile
from pydub import AudioSegment

# Đọc file âm thanh từ thư mục './samples/' và chuyển đổi sang định dạng WAV
sound = AudioSegment.from_file("./queries/ĐẦU TIÊN FANCAM.mp3", format="mp3")
sound.export("./queries/recording.wav", format="wav")

# Đọc file âm thanh WAV
sampling_rate, data = wavfile.read('./samples/recording.wav')

# Chuyển đổi dữ liệu âm thanh sang kiểu số thực và chuẩn hóa độ lớn về [-1, 1]
data = data / 32767.0

# Áp dụng bộ lọc thông qua FFT để loại bỏ tiếng ồn
fft_data = np.fft.fft(data)
frequencies = np.fft.fftfreq(len(data), 1 / sampling_rate)
mask = (frequencies > 0) & (frequencies < 5000)
fft_data_filtered = fft_data.copy()
fft_data_filtered[np.abs(frequencies) > 5000] = 0
fft_data_filtered[mask] = signal.wiener(np.abs(fft_data_filtered[mask]))

# Chuyển đổi dữ liệu âm thanh trở lại dạng tín hiệu trong miền thời gian
filtered_data = np.fft.ifft(fft_data_filtered).real

# Chuẩn hóa lại độ lớn của dữ liệu âm thanh
filtered_data = filtered_data / np.max(np.abs(filtered_data))

# Ghi file âm thanh sau khi lọc vào thư mục './samples/'
wavfile.write('./samples/filtered.wav', sampling_rate, np.int16(filtered_data * 32767))
