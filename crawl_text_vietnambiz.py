from bs4 import BeautifulSoup
import requests
import json
import os

if os.path.exists('news_links_vietnambiz_1.json'):
    with open('news_links_vietnambiz_1.json', 'r', encoding='utf-8') as f:
        data = json.load(f)


def crawl_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    extracted_text = ""
    sapo_div = soup.find("div", class_="vnbcbc-sapo")
    if sapo_div:
        # Append the text within this div to the string
        extracted_text += sapo_div.get_text(strip=True)
    content_div = soup.find('div', class_=lambda value: value and ('vnbcbc-body vceditor-content' in value))
    p_tags = content_div.find_all("p")
    for p in p_tags:
        # Append the text within each p tag to the string
        extracted_text += p.get_text(strip=True)

    # get tag
    item_tags = []
    div_tag = soup.find("div", class_="vnbcbcbs-tags")
    if div_tag:
        tags = div_tag.find_all("li")
        for tag in tags:
            item_tags.append(tag.get_text(strip=True))
    return extracted_text, item_tags


def loop_item(start, end):
    for i in range(start, end):
        print("Item", i)
        text, item_tags = crawl_text(data[i]['Link'])
        print(text)
        print(item_tags)


number_of_item = len(data)
loop_item(1, 20)
