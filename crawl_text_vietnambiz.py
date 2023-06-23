from bs4 import BeautifulSoup
import requests
import json
import os


def crawl_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    extracted_text = ""
    sapo_div = soup.find("div", class_="vnbcbc-sapo")
    if sapo_div:
        # Append the text within this div to the string
        extracted_text += sapo_div.get_text(strip=True)
    content_div = soup.find('div', class_=lambda value: value and ('vnbcbc-body vceditor-content' in value))
    if not content_div:
        return None, None
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
        # guard
        if i >= number_of_item:
            break
        print("Item", i)

        text, item_tags = crawl_text(data[i]['Link'])
        if text is None and item_tags is None:
            continue
        print(text)
        print(item_tags)
        item = {
                'Title': data[i]['Title'],
                'Content': text,
                'Tags': item_tags
        }
        if item not in output:
            output.append(item)
        else:
            print("skip")


if os.path.exists('news_links_vietnambiz_1.json'):
    with open('news_links_vietnambiz_1.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
number_of_item = len(data)

if os.path.exists('data_vietnambiz_test.json'):
    print("---- Continue ----")
    with open('data_vietnambiz_test.json', 'r', encoding='utf-8') as f:
        output = json.load(f)
else:
    output = []
loop_item(len(output), len(output) + 100)
with open('data_vietnambiz_test.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=4)




