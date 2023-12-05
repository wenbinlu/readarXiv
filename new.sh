#!/bin/zsh

conda activate my_Python
python pull_abstracts.py
python makeaudio.py

# to run this shell script, follow these two steps:
# one: chmod +x new.sh  (this step only needs to be done once and for all)
# two: source new.sh (this will first activate a conda environment which contains preinstalled packages like 'numpy', 'arxiv', and 'openai'; then two Python codes will be run in sequence)
