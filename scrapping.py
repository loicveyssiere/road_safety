import numpy as np 
import requests as requests
import re as re
import os as os
import json as json 
from bs4 import BeautifulSoup

url_base = 'https://www.data.gouv.fr/fr/datasets/base-de-donnees-accidents-corporels-de-la-circulation/'
regex_base = '(vehicules|usagers|lieux|caracteristiques)_20..\.csv'
dir_data = 'data/'

if not os.path.isdir(dir_data):
    os.makedirs(dir_data)

    # -------------------------------------------------------------------------
    # HERE NETWORK CALL - DO NOT ABUSE
    r = requests.get(url_base)
    # -------------------------------------------------------------------------

    soup = BeautifulSoup(r.text, 'html.parser')

    files = []

    # Extraction of data urls
    soup.find_all('a')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href is not None:
            m = re.search(regex_base, href)
        else:
            m = None
        if m is not None:
            name = m.group(0)
            info = name.split('_')
            type = info[0]
            year = info[1].replace('.csv', '')
            if (len(info) is not 2):
                print('Oh damn! That was unexpected ...')
            else:
                files.append({'name': name, 'type': type, 'year': year, 'url': href})

    # store information file
    with open(dir_data + 'info.json', 'w') as f:
        json.dump(files, f)

    # imports of different files
    for i, file in enumerate(files):
        path = dir_data + file['name']
        if not os.path.isfile(path):
            # ------------------------------------------------------------------------------
            # HERE NETWORK CALL - DO NOT ABUSE
            r = requests.get(file['url'])
            # ------------------------------------------------------------------------------
            
            with open(path, 'w') as f:
                f.write(r.text)


else:
    print('A data folder already exists, the process has been avorted to avoid useless server calls')
