import sys


log_file = open("result.txt", "w")

stdout_backup = sys.stdout

sys.stdout = log_file
