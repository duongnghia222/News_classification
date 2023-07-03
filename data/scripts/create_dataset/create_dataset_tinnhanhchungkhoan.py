import json
import requests
from bs4 import BeautifulSoup
import os

# Đọc file json chứa link


# Danh sách để lưu nội dung từ các link
data_all =[]
contents = []

# Lấy link từ từng item
with open('./data/label/label_tinnhanhchungkhoan.json', 'r', encoding='utf-8-sig') as file:  # Thêm '-sig' để tự động loại bỏ BOM
    data = json.load(file)
    
for item in data:

    content = item['Content']
    title = item['Title']
    headline = item['Headlines']
    label = item['Label']
    
    all_content = title + headline + content
    # Thêm nội dung vào danh sách
    contents.append({
        'Content': all_content,
        'Label': label
    })
    
    
    
data_all.extend(contents)

# Ghi nội dung đã lấy được vào file json mới
with open('./data/raw_data/raw_data_tinnhanhchungkhoan.json', 'w', encoding='utf-8') as file:
    json.dump(data_all, file,ensure_ascii=False,indent=4)
