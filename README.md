I have a long home-to-work commute, during which I would like to listen to daily 'news' on the axXiv.

This project creates a large number of .mp3 files according to the newly posted abstracts on "arXiv/astro-ph/new" and then plays them in sequence. The Replacements are ignored. When each .mp3 is played, the user has 30 seconds (adjustable) to make a decision whether to save the arxiv-ID of this abstract or not. In the end, a list of the saved arxiv-IDs will be printed.

If you just want to listen to the .mp3 files (because producing them daily costs about 2 US dollars), you can download the updated files 

Prerequisite: openAI (and an API key to make payment), pygame, glob

There are four steps:

(1) one must change the 'datadir' variable in "dir_info.py" to wherever the data will be saved. You also need an API key from openAI, which should be placed in your .zshrc (or .bashrc) file in the following form:

export OPENAI_API_KEY="..."

(2) run "python pull_abstracts.py", which will pull all the abstracts from the "arXiv/astro-ph/new" website (one can change the website into a different one).

(3) run "python makeaudio.py", which converts all the abstract files ('.txt') into audio files ('.mp3'). Each file takes about 1 minute to process, mostly because the openAI client takes a while to respond to each request. However, if you have multiple cores (as specified by 'Ncpu'), this process can speed up linearly with the number of logical cores.

(4) Finally, run "python run_playaudio.py", which will play the .mp3 files one by one. For each .mp3 file, the user has 30 seconds (an adjustable parameter in 'playaudio.py') to decide whether to save the arxiv-ID for this file. Alternatively, one can download the .mp3 files into a smartphone or something else with an audio player.

Enjoy!

Todo list:

(1) Currently, only the newest papers can be listened. I hope to make "today" an arbitrary day by using the content on "http://dailyarxiv.com", so the user can listen to the arxiv papers posted on any day.

(2) I would like to create a nicer interface with buttons to click, instead of having to use a keyboard while listening.

(3) The most expensive part of is the text-to-speech conversion using openAI (roughly a few US cents per abstract). I hope to replace this part with free TTS codes such as, https://github.com/mozilla/TTS (not sure if this is free) or https://github.com/nateshmbhat/pyttsx3

(4) Some math expressions need to be processed into plain text. For instance, "$\beta/\alpha$" should be 'beta over alpha'. This can in principle be done with MathJax.