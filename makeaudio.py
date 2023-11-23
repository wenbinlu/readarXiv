from openai import OpenAI
import time
from glob import glob
from dir_info import *
import subprocess
start_time = time.time()

client = OpenAI()
skip_generate = False

savedir = datadir + today + '/'
all_files = glob(savedir + '*.txt')
id_list = [f.replace(savedir, '').replace('.txt', '') for f in all_files]

print(id_list)
for arxiv_id in id_list:
    abstr_fname = savedir + arxiv_id + '.txt'
    audio_savename = savedir + arxiv_id + '.mp3'
    system_cont = 'You are a professional astrophysicist.'\
                  'You will be provided with the title and the abstract of a paper.'\
                  'Please provide an expert-level, brief summary,'\
                  'including the main methods and findings.'\
                   + 'Please include the title at the beginning of your response.'

    # read the abstract
    with open(abstr_fname, 'r') as f:
        abstr = f.readline()

    if not skip_generate:
        # create a digest
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_cont},
                {"role": "user", "content": abstr}
            ]
        )

        response_txt = completion.choices[0].message.content
        print('\n---The generated text:\n', response_txt)

        # convert txt to audio
        response_audio = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=response_txt,
        )

        # save the audio to a file
        response_audio.stream_to_file(audio_savename)

    # --- convert to wav for better reading (there is no need for this)
    #subprocess.call(['ffmpeg', '-loglevel', 'quiet', '-y',
    #                 '-i', audio_savename, '-c:a', 'libvorbis',
    #                 '-q:a', '10',
    #                 audio_savename.replace('.mp3', '.wav')])
    
