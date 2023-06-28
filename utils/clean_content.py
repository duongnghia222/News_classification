import re
import json


def clean_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    for d in data:
        d['Content'] = re.sub(r'\u00A0', ' ', d['Content'])

    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


clean_content("../data/contents/data_vietnambiz_1_2.json")
