#!/bin/zsh

conda activate my_Python

if [ $# -eq 1 ]; then
    today=$1
else
    today=$(date +%Y-%m-%d)   # use the current date
fi

python write_date.py $today   # write into 'date_info.py'

use_iarxiv=1   # change this to '1' to use iarxiv ('0' else)
if [ $use_iarxiv -eq 0 ]; then
    python pull_abstracts.py  # most recent abstracts without sorting by preference
else
    python iarxiv.py   # abstracts sorted by preference
fi

python makeaudio.py

# to run this shell script, follow these two steps:
# one: chmod +x new.sh  (this step only needs to be done once and for all)
# two: source new.sh 2023-12-23
# this will first activate a conda environment which contains preinstalled packages like 'numpy',
# 'arxiv', 'openai', 'selenium', 'bs4'; then some Python codes will be run in sequence. If a date is  not specified, then the default date is today
