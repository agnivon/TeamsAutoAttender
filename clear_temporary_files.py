import os
import shutil


def delete_temp_files():
    temp_folders = list(filter(lambda x: x.startswith('.com.google.Chrome'), os.listdir('/tmp')))
    for temp_folder in temp_folders:
        shutil.rmtree(os.path.join("/tmp/", temp_folder), ignore_errors=True)


delete_temp_files()
