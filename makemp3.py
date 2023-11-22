from openai import OpenAI
from playsound import playsound
import time
from datetime import datetime
from glob import glob
from dir_info import *
start_time = time.time()

client = OpenAI()

today = datetime.today().strftime('%Y-%m-%d')
all_files = glob(fdir + today + '/*.txt')
id_list = [f.replace(fdir + today + '/', '').replace('.txt', '') for f in all_files]

print(id_list)

exit()
abstr_fname = arxiv_id + '.txt'
audio_savname = arxiv_id + '.mp3'
cont_command = 'Provide a short summary for the following abstract of a recent paper,' \
               'including the main methods and findings. ' \
               'Please include the title.'\
               + 'Keep in mind that your audience is an astrophysicist expert.'

# read the abstract
with open(fdir + abstr_fname, 'r') as f:
    abstr = f.readline()

# create a digest
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a professional astrophysicist."},
    {"role": "user", "content": cont_command},
    {"role": "user", "content": abstr}
  ]
)

response_txt = completion.choices[0].message.content
print('---The generated text:', response_txt)

# convert txt to audio
response_audio = client.audio.speech.create(
  model="tts-1",
  voice="alloy",
  input=response_txt,
)

# save the audio to a file
response_audio.stream_to_file(fdir + audio_savname)

mid_time = time.time()
print("---It took %s seconds to make the .mp3 file" % (mid_time - start_time))

# play the mp3 file
playsound(fdir + audio_savname)

end_time = time.time()
print("---It took %s seconds to play the audio" % (end_time - mid_time))
