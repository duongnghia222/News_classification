import json


def create_index_field(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # loop through each item and add an index
    for i, item in enumerate(data):
        item['Index'] = i

    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


create_index_field("../data/contents/data_vietnambiz_1_1.json")


