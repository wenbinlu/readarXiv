from playsound import playsound
from datetime import datetime
from glob import glob
from dir_info import *

today = datetime.today().strftime('%Y-%m-%d')
all_files = glob(fdir + today + '/*.txt')
id_list = [f.replace(fdir + today + '/', '').replace('.txt', '') for f in all_files]

print(id_list)

for id in id_list:
    audio_savname = id + '.mp3'
    playsound(fdir + today + '/' + audio_savname)