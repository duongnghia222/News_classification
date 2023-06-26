import json

def remove_duplicates_items(file_path):
    # Step 1: Read JSON file and load contents into a Python object
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    # Step 2: Identify and remove duplicate items from the object
    unique_data = list(set(json.dumps(item, sort_keys=True) for item in data))
    unique_data = [json.loads(item) for item in unique_data]

    # Step 3: Write the updated object back to the JSON file
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(unique_data, json_file, ensure_ascii=False, indent=4)

# Usage example
# remove_duplicates_items('news_links_tinnhanhchungkhoan.json')
remove_duplicates_items('./data/contents/data_vietstock.json')
remove_duplicates_items('./data/contents/data_vietnambiz_1_1.json')
remove_duplicates_items('./data/contents/data_vietnambiz_1_2.json')
remove_duplicates_items('./data/contents/data_nguoiquansat.json')

