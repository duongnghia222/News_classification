import json
import re

# Đọc file json chứa bài báo
with open('./data/contents/data_tinnhanhchungkhoan.json', 'r', encoding='utf-8-sig') as file:
    data = json.load(file)

# Biểu thức chính quy tìm các từ có 3 chữ cái bao quanh bởi dấu ngoặc tròn
pattern = r'\([a-zA-Z]{3}\)'

label_arti = []

for article in data:
    # Lấy title của bài báo
    title = article['Title']
    print(type(title))
    if isinstance(title,list):
        print(title)
        print(article['Link'])

    # Tìm các từ phù hợp trong title
    matches = re.findall(pattern, title)

    if matches:
        # Lấy từ đầu tiên tìm được, bỏ qua các dấu ngoặc tròn
        label = matches[0][1:-1]  # Bỏ qua dấu ngoặc tròn đầu và cuối

        # Thêm label vào bài báo
        article['Label'] = label
        label_arti.append(article)
        #i=1
    else:
        headlines = article['Headlines']
        matches = re.findall(pattern,headlines)
        if matches:
            label = matches[0][1:-1]
            
            article['Label'] = label
            label_arti.append(article)
        else:
            tags = article['Tag']
            for a in tags:
                if len(a) ==3:
                    article['Label'] = a
                    label_arti.append(article)
                    continue
            tag = ' '.join(tags)
            matches = re.findall(pattern,tag)
            if matches:
                label = matches[0][1:-1]
            
                article['Label'] = label
                label_arti.append(article)
            else:
                content = article['Content']
                
            
            
        

# Ghi dữ liệu đã cập nhật vào file json mới
with open('./data/label/data_tinnhanhchungkhoan.json', 'w', encoding='utf-8') as file:
    json.dump(label_arti, file, ensure_ascii=False,indent=4)
