import os
import json
import requests
from fake_useragent import UserAgent
from tqdm import tqdm
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
}

ua = UserAgent()
FAKE_HEADERS = {
    'User-Agent': ua.chrome
}

def crawl_text_and_tags(url, headers= HEADERS):
    response = requests.get(url, headers= headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    def crawl_text():
        nonlocal soup
        news_content = ""
        information = soup.find("div", {"id": "vst_detail"})
        if information:
            information = information.find_all("p")
            for passage in information:
                if passage.get('class') is None:
                    print("")
                elif passage.get('class')[0] not in ['pTitle', "pAuthor", "pSource"]:
                    if news_content:
                        news_content += ' '
                    news_content += passage.text
        return news_content
    def crawl_tags():
        nonlocal soup
        news_tags = []
        try:
            tag_elements = (soup.find("div", class_="tags mt20")).find_all("li")
            if len(tag_elements) > 0:
                for tag in tag_elements:
                    if tag.get('class') is None:
                        news_tags.append(tag.text.strip())
        except:
            print("DON'T HAVE TAGS")
        return news_tags     
    return crawl_text(), crawl_tags()

with open('./data/links/news_link_vietstock.json', 'r', encoding='utf-8') as f:
    data =json.load(f)

result = []

for idx in tqdm(range(len(data))):
    main_content, tags = crawl_text_and_tags(data[idx]['link'])
    dictionary = {
        'Title': data[idx]['title'],
        'Content': main_content,
        'Tags': tags,
        'Index': idx
    }
    result.append(dictionary)

if os.path.exists('./data/contents/data_vietstock.json'):
    os.remove('./data/contents/data_vietstock.json')

with open('./data/contents/data_vietstock.json', 'w+', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
