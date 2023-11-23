import subprocess
from glob import glob
from dir_info import *
import os

# this calls "playaudio.py" repetitively for each .mp3 file

savedir = datadir + today + '/'
fmt = '.mp3'
all_files = glob(savedir + '*' + fmt)
id_list = [f.replace(savedir, '').replace(fmt, '') for f in all_files]

print(id_list)
save_id_list = []

#os.chdir(codedir)
for arxiv_id in id_list:
    audio_savename = savedir + arxiv_id + fmt
    print('playing ' + arxiv_id)
    res = subprocess.check_output('python ' + codedir + 'playaudio.py ' + audio_savename,
                                  shell=True)
    s = res.decode("utf-8")
    if s[0] == 'Y':
        save_id_list += [arxiv_id]

# finally print out the ones that are interesting
print('The following are interesting:')
print(save_id_list)
    
        
