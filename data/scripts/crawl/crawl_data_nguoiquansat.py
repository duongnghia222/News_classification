import json
import requests
from bs4 import BeautifulSoup

# Đọc file json chứa link


# Danh sách để lưu nội dung từ các link
data_all =[]
contents = []

    # Lấy link từ từng item
with open('./data/links/news_link_nguoiquansat.json', 'r', encoding='utf-8-sig') as file:  # Thêm '-sig' để tự động loại bỏ BOM
    data = json.load(file)
    
for item in data:
    
    link = item['Link']
    response = requests.get(link)

    # Sử dụng BeautifulSoup để phân tích nội dung HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Tìm tất cả thẻ <p> có class "Headlines" và biến đổi thành text
    p_tags = soup.find('p', class_='Headlines')
    headlines = p_tags.get_text() 
    
    # Lấy article
    articles = soup.find('h1', class_='c-detail-head__title')
    
    title = articles.get_text() 
    
    #Lấy tag cũng như đoạn text chính
    div_tags = soup.find('div', class_ = 'entry')
    
    content = []
    highlight_tags = []    
        
    if div_tags:

        highlight_tags =  div_tags.find_all('a', href=True, attrs={'target': '_blank'})
        highlight_tags = [a.get_text().replace(u'\ufeff', '') for a in highlight_tags]
        if highlight_tags:
            if len(highlight_tags) !=1:
                highlight_tags.pop()
      
        for a in div_tags.find_all('a', href=True, attrs={'target': '_blank'}):
            a.unwrap()

        div_tag = div_tags.find_all('p')
        content = [p.get_text().replace(u'\ufeff', '')  for p in div_tag]
        content.pop()
        
    else:
        content = []
    
    # Thêm nội dung vào danh sách
    contents.append({
        'Link': link,
        'Title':title,
        'Headlines': headlines,
        'Content': content,
        'Tag': highlight_tags
    })
    
    
data_all.extend(contents)

# Ghi nội dung đã lấy được vào file json mới
with open('./data/contents/data_nguoiquansat.json', 'w+', encoding='utf-8') as file:
    json.dump(data_all, file,ensure_ascii=False,indent=4)
