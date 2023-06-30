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
        if 'show-placeholder' in p.get('class', []) or 'NLPlaceholderShow' in p.get('class', []):
            continue
        text = " " + p.get_text(strip=False)
        # Append the normalized text within each p tag to the string, replacing NNBS with a space
        extracted_text += text.replace('\xa0', ' ').replace('\u00A0', ' ')

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
        item = {
                'Title': data[i]['Title'],
                'Content': text,
                'Tags': item_tags
        }
        if item not in output:
            output.append(item)
        else:
            print("skip")


from_file = '../../links/news_link_vietnambiz_1.json'
to_file = '../../contents/data_vietnambiz_1.json'

if os.path.exists(from_file):
    with open(from_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
number_of_item = len(data)

if os.path.exists(to_file):
    print("---- Continue ----")
    with open(to_file, 'r', encoding='utf-8') as f:
        output = json.load(f)
else:
    output = []
loop_item(len(output), len(output) + 5000)
with open(to_file, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=4)




