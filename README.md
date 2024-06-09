I have a long commute to work, during which I sometimes would like to listen to daily 'news' on the axXiv.

This project creates a large number of .mp3 files according to abstracts on the arXiv and then plays them in sequence. When each .mp3 is played, the user has 30 seconds (adjustable) to make a decision whether to save the arxiv-ID of this abstract or not. In the end, a list of the saved arxiv-IDs will be printed.

If you ONLY want to listen to the .mp3 files without producing them, you can download the files by going to [this link](https://www.dropbox.com/scl/fo/i3ty75f8mzmaqdo780bwb/AJCSavAiFkjmtmOxr1i9pnA?rlkey=vd98ylvn58t7tdksd1scjgxux&st=qiryv96o&dl=0). Note that old files in the distant past will be removed to save storage space.

If you want to generate the .mp3 files by yourself, follow the steps below. With the current implementation, it costs about 2 US dollars to process all the newly posted abstracts per day.

Prerequisite: openAI (and an API key to make payment), pygame, glob

An alternative source of abstracts is 'iarxiv.org' hosted by E. Alvarez, C. Miquel and collaborators. The advantages of this choice are (i) the abstracts can be ranked according to your preference, (ii) the date can be sepecified. The additional requirements are 'selenium' and 'bs4' packages.

Follow these steps:

(1) one must change the 'datadir' variable in "dir_info.py" to where you want the data to be saved and the 'codedir' variable to the cloned Github directory.

(2) You need an API key from openAI, which should be placed in your .zshrc (or .bashrc) file in the following form:

export OPENAI_API_KEY="..."

(3) 'python write_date.py DATE', where DATE='YYYY-MM-DD' specifies the date for the abstracts. A weekend date is avoided by shifting to the previous Friday.

(4) 'python iarxiv.py', which pulls the abstracts posted on the date specified in 'date_info.py'. For this to work, you need to have an account at iarxiv.org, and then put your credentials in a file called "credentials_iarxiv.py" in the format of 'username=EMAIL' and 'password=PASSWORD' in two separate lines. The website iarxiv.org allows the user to rank papers according to their scores, and this requires the user to train the machine by clicking the links to papers for a while (e.g., a week). In the end, you can change 'score_min' in iarxiv.py to reflect the minimum score below which you will discard the papers as they are likely less interesting to you.

It takes about 40 seconds to run iarxiv.py, because the website takes a while to return a list of abstracts. Sometimes, there are no papers on a given weekday (because it is a local holiday) and the code will return "Please enter a different date!". Go back to Step (3).

Alternatively, you can run "python pull_abstracts.py", which will pull the most recent abstracts from the "arXiv/astro-ph/new" website. This does not require an account at iarxiv.org, but the abstracts are not ranked.

(5) 'python makeaudio.py', which converts all the abstract files ('.txt') into audio files ('.mp3'). Each file takes about 1 minute to process, mostly because the openAI client takes a while to respond to each request. However, if you have multiple cores (as specified by 'Ncpu'), this process can speed up linearly with the number of logical cores.

The above steps are put together in one line of code:

'source new.sh DATE' (to specify a date in the format YYYY-MM-DD) or simply 'source new.sh' (default to the current day). For the first time, you need to do 'chmod +x new.sh' to change the file mode.


(6) Finally, run "python run_playaudio.py", which will play the .mp3 files one by one. For each .mp3 file, the user has 30 seconds (an adjustable parameter in 'playaudio.py') to decide whether to save the arxiv-ID for this file. Alternatively, one can download the .mp3 files into a smartphone or something else with an audio player.

Enjoy!


Todo list:

(1) I hope to add the possibility of pulling abstracts from "http://dailyarxiv.com".

(2) I hope to create a nicer interface with buttons to click, instead of having to use a keyboard while listening.

(3) The most expensive part of is the text-to-speech conversion using openAI. I hope to replace this part with free TTS codes such as, https://github.com/mozilla/TTS (not sure if this is free) or https://github.com/nateshmbhat/pyttsx3

(4) Some math expressions need to be processed into plain text. For instance, "$\beta/\alpha$" should be 'beta over alpha'. This can in principle be done with MathJax.