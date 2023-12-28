import urllib.request as libreq
import re
import arxiv
import os
from datetime import datetime

from dir_info import *

today = datetime.today().strftime('%Y-%m-%d')
url = 'https://arxiv.org/list/astro-ph/new'
savedir = datadir + today + '/txt/'

if not os.path.exists(savedir):
    os.makedirs(savedir, exist_ok=True)

len_ident = 16   # length of the identifier (16)
id_list = []
with libreq.urlopen(url) as f:
    data = f.read().decode('utf-8')
    # grab all the arXiv numbers before the replacements
    ind_rep = data.find('Replacements for')
    target_str = 'arXiv:'
    inds = [m.start() for m in re.finditer(target_str, data[:ind_rep])]
    for i in inds:
        arxiv_id = data[i:i+len_ident].replace('arXiv:', '')
        # make sure a PDF is available for this paper
        if 'pdf/'+arxiv_id in data[i+len_ident:i+len_ident+100]:
            # print(arxiv_id)
            id_list += [arxiv_id]
    print('number of new papers:', len(id_list))

# Construct the default API client.
client = arxiv.Client()

# search for all the new papers
search_by_id = arxiv.Search(id_list=id_list)

results = client.results(search_by_id)

i = 0
for r in results:
    arxiv_id = id_list[i]
    i += 1
    with open(savedir + '%03d' % i + '.txt', 'w') as f:
        f.write('title: ' + r.title + '\n')
        authors = [str(aut) for aut in r.authors[:2]]
        f.write('authors: ' + ', '.join(authors[:2]) + '\n')
        f.write('abstract: ' + r.summary + '\n')
