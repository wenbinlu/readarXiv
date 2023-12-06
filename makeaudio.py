from openai import OpenAI
from glob import glob
from dir_info import *
import numpy as np
import multiprocessing
from multiprocessing import Process

client = OpenAI()

savedir = datadir + today + '/'
all_files = glob(savedir + 'txt/*.txt')
id_list = [f.replace(savedir + 'txt/', '').replace('.txt', '') for f in all_files]
Nid = len(id_list)

# number of logical cores
Ncpu = min(Nid, multiprocessing.cpu_count())
np.random.seed(31171)

#gptmodel = 'gpt-3.5-turbo'
gptmodel = 'gpt-4'

# the following controls the output from ChatGPT
system_cont = 'You are a professional astrophysicist.'\
    'You will be provided with the title and then the abstract of a research paper.'\
    'Please provide an expert-level, brief summary,'\
    'including the main methods and findings.'\
    + 'Please restrict your response to less than 150 words.' \
    ' Please include the title (but not the abstract) at the beginning of your response.'


def makemp3(jlist, s):  # s is a random number (not used)
    for j in jlist:
        makemp3_one(id_list[j])

        
def makemp3_one(arxiv_id):
    abstr_fname = savedir + 'txt/' + arxiv_id + '.txt'
    audio_savename = savedir + arxiv_id + '.mp3'

    # read the abstract
    with open(abstr_fname, 'r') as f:
        abstr = f.readline()

    # create a digest
    completion = client.chat.completions.create(
        model=gptmodel,
        messages=[
            {"role": "system", "content": system_cont},
            {"role": "user", "content": abstr}
        ]
    )
    response_txt = completion.choices[0].message.content
    print('\n---' + arxiv_id + ':\n', response_txt)
    # --- convert txt to audio
    response_audio = client.audio.speech.create(
        model="tts-1",
        voice=np.random.choice(['alloy', 'fable', 'nova', 'shimmer']),
        input=response_txt,
        )
    # --- save the audio to a file
    response_audio.stream_to_file(audio_savename)


if __name__ == '__main__':
    print(id_list)
    print('number of CPUs used', Ncpu)
    # divide the task into Ncpu chunks
    jlist_chunks = np.array_split(range(Nid), Ncpu)
    procs = [Process(target=makemp3,
                     args=(jlist_chunks[n], np.random.randint(10)))
             for n in range(Ncpu)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()


# --- convert mp3 to wav (there is no need for this)
# subprocess.call(['ffmpeg', '-loglevel', 'quiet', '-y',
#                 '-i', audio_savename, '-c:a', 'libvorbis',
#                 '-q:a', '10',
#                 audio_savename.replace('.mp3', '.wav')])
