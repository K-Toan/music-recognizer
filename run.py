from database import store, delete
from process import recognize


# path
samples_path = "./samples/"
queries_path = './queries/'

# database
# delete.delete_all()
store.store_samples(samples_path)

# recognize song
recognize.recognize_multiple_songs(queries_path)