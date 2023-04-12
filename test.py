from database import store
from process.recognize import *
from process.recognise import *

# database
samples_path = "./samples"
store.store_samples(samples_path)

print(recognize_song("test_samples/Cut1.mp3"))

