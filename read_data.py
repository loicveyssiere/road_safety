import numpy as np 
import pandas as pd
import json as json

dir_data = 'data/'

 # read information file
info = None
with open(dir_data + 'info.json', 'r') as f:
    info = json.load(f)

path = dir_data + info[0]['name']

df = pd.read_csv(path, delimiter=',')

print(df.head())
