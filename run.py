import os
import glob
from database import store, delete
from process import recognize


# database
samples_path = "./samples_test/"
delete.delete_all()
store.store_samples(samples_path)

# Đường dẫn đến thư mục cần so sánh
queries_path = './queries_test/'

# Liệt kê các file trong thư mục
for file_path in glob.glob(os.path.join(queries_path, '*')):
    print(f"\n---------------Comparing {os.path.basename(file_path)}---------------")
    if os.path.isfile(file_path):
        recognize.recognize_song(queries_path + os.path.basename(file_path))
