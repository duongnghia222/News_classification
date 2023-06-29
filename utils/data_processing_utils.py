import json
import re
import pandas as pd


def split_json(filepath, file1_name, file2_name):
    # Load the data from the large file
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Find the midpoint of the data
    midpoint = len(data) // 2

    # Split the data into two halves
    data1 = data[:midpoint]
    data2 = data[midpoint:]

    # Write the first half of the data to a new file
    with open(file1_name, 'w', encoding='utf-8') as f:
        json.dump(data1, f, ensure_ascii=False, indent=4)

    # Write the second half of the data to another new file
    with open(file2_name, 'w', encoding='utf-8') as f:
        json.dump(data2, f, ensure_ascii=False, indent=4)


def create_index_field(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # loop through each item and add an index
    for i, item in enumerate(data):
        item['Index'] = i

    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


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


def clean_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    for d in data:
        d['Content'] = re.sub(r'\u00A0', ' ', d['Content'])

    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def predict_label(text, tags):
    list_stock_codes = []
    df_hose_tickers = pd.read_csv('../data/tickers/hose_tickers.csv')
    df_hnx_tickers = pd.read_csv('../data/tickers/hnx_tickers.csv')
    df_uc_tickers = pd.read_csv('../data/tickers/uc_tickers.csv')
    list_stock_codes.extend(df_hose_tickers['Stock Code'].tolist())
    list_stock_codes.extend(df_hnx_tickers['Stock Code'].tolist())
    list_stock_codes.extend(df_uc_tickers['Stock Code'].tolist())
    for tag in tags:
        if tag.upper() in list_stock_codes:
            return str(tag).upper()
    matches = re.findall(r"(?i)\bMã:\s{0,2}([A-Z0-9]{3})", text)
    if len(matches) >= 3:
        return ""
    for match in matches:
        if match in list_stock_codes:
            print(match.upper())
            return str(match).upper()
    return ""


def assign_label(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for d in data:
        d["Label"] = predict_label(d["Content"], d['Tags'])
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def export_raw_data(filepath, export_dir):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    new_data = []
    for d in data:
        if d["Label"] != "":
            new_data.append({
                "Content": d["Title"] + d["Content"],
                "Label": d["Label"]
            })

    with open(export_dir, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)

export_raw_data("../data/contents/data_vietnambiz_1_2.json", "../data/raw_data/raw_data_vietnambiz_2.json")


# assign_label("../data/contents/data_vietnambiz_1_1.json")
# create_index_field("../data/label/label_tinnhanhchungkhoan.json")
# predict_label(" (Mã: PNJ)", [])