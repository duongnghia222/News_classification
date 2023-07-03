import sys
import os

from tqdm import tqdm
import json
import re

get_label_path = './data/label/label_vietstock_final.json'
raw_data_path = './data/raw_data/raw_data_vietstock.json'

with open(get_label_path, 'r', encoding= 'utf-8') as f:
    data = json.load(f)

def return_index(x):
    return x['Index']
data = sorted(data, key= return_index)

result_data = []
for item in data:
    if (item['Label'] == ""): continue
    dictionary = {
        "Content": item['Title'] + '. ' + item['Content'],
        "Label": item['Label'] 
    }
    result_data.append(dictionary)

if os.path.exists(raw_data_path):
    os.remove(raw_data_path)

with open(raw_data_path, 'w+', encoding='utf-8') as f:
    json.dump(result_data, f, ensure_ascii=False, indent= 4)
