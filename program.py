import os
import glob
import re

folder_name = 'C:/Users/User/Desktop/songs/'

for name in glob.glob('C:/Users/User/Desktop/songs/*'):
    name_splitted = name.split('\\')
    file_name = name_splitted[-1]
    file = file_name.split('-')
    if len(file) > 2:
        file = file[1]
        file = file.lstrip()
    os.rename(name, f"{folder_name}/{file}.mp3")
print('DONE!')