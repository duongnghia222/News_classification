import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'utils'))
import get_ticker

from tqdm import tqdm
import json
import re

ticker = get_ticker.get_ticker(get_market=False)
get_data_path = './data/contents/data_vietstock.json'
save_path = './data/raw_data/raw_data_vietstock.json'

hnx_pattern = r'HNX:\s[A-Z][A-Z0-9]{2}'
hose_pattern = r'HOSE:\s[A-Z][A-Z0-9]{2}'
upcom_pattern = r'U[pP][cC][o][mM]:\s[A-Z][A-Z0-9]{2}'
ticker_pattern = r'[A-Z][A-Z0-9]{2}'

def replace_space(stock_list):
    """
        Loại bỏ kí tự \xa0 được lấy từ regex
    """
    return list(map(lambda x: (x.replace(u'\xa0', u' ').encode('utf-8')).decode(), stock_list))

def get_label(readfile_path, writefile_path = None):
    with open(readfile_path, mode='r', encoding='utf-8') as f:
        data = json.load(f)

    write_result = []
    length = len(data)
    label = []
    count = 0
    count_no_label = 0
    for i in tqdm(range(length)):
        # if i != 3316: continue
        add_label = ""
        input = data[i]['Content']
        hose_lst = re.findall(pattern=hose_pattern, string=input)
        hnx_lst = re.findall(pattern=hnx_pattern, string=input)
        upcom_lst = re.findall(pattern=upcom_pattern, string=input)
        if len(hose_lst) + len(hnx_lst) + len(upcom_lst) == 0:
            count_no_label += 1
            # continue
        elif len(hose_lst) + len(hnx_lst) + len(upcom_lst) == 1:
            add_label = None
            if len(hose_lst) == 1: add_label = hose_lst
            elif len(hnx_lst) == 1: add_label = hnx_lst
            else: add_label = upcom_lst
            # print(replace_space(add_label)[0])
            add_label = replace_space(add_label)[0][-3:]
        else:
            count += 1
            tags = data[i]['Tags']
            # print(tags)
            # print(input)
            ticker_codes = []
            for tag in tags:
                tag_code = re.findall(pattern=ticker_pattern, string=tag)
                # print(tag_code)
                if len(tag_code) > 0:
                    if tag_code[0] in ticker:
                        ticker_codes.append(tag_code[0])
                        # print("DA APPEND")
            ticker_codes = list(set(ticker_codes))
            title = data[i]['Title']
            if len(ticker_codes) == 1:
                add_label = ticker_codes[0]
                # print("TAGSSSS")
                # print(input, tags)
            else:
                for tk_code in ticker_codes:
                    title_code = re.findall(pattern=f'({tk_code})', string=title)
                    if len(title_code) > 0:
                        add_label = title_code[0]
                        # print("TUEUEURUURUER")
                        # print(input, tags, title)
                        # print(title_code[0])
                        break
        label.append(add_label)
        # print(label[-1])
        write_result.append({
            'Title': data[i]['Title'],
            'Content': input,
            'Tags': data[i]['Tags'],
            'Label': add_label,
            "Index": i
        })
    # print(count)
    # print(count_no_label)
    if writefile_path:
        
        if os.path.exists(writefile_path):
            os.remove(writefile_path)
        with open(writefile_path, 'w+', encoding='utf-8') as f:
            json.dump(write_result, f, ensure_ascii=False, indent=4)        
    return label

get_label(get_data_path, save_path)