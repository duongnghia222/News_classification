from bs4 import BeautifulSoup
import requests
import json
from urllib.parse import urljoin
import os
from datetime import datetime

# Function to parse the HTML and extract the desired data
def parse_html(url, from_time="11:40 | 19/06/2029"):
    """

    :param url:
    :param from_time: get article from (from_time : the past)
    :return:
    """
    from_time = datetime.strptime(from_time, "%H:%M | %d/%m/%Y")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []
    base_url = 'https://vietnambiz.vn/'
    list_news_divs = soup.find_all('div', class_='list-news')  # Find the div with class 'list-news'
    for list_news_div in list_news_divs:
        articles = list_news_div.find_all('div', class_='item')  # Find 'item' divs within 'list-news' div
        for article in articles:
            item_time = article.find('span', class_='timeago need-get-timeago').get_text(strip=True)
            article_time = datetime.strptime(item_time, '%H:%M | %d/%m/%Y')
            if article_time >= from_time:
                continue
            title = article.find('h3', class_='title').text.strip()
            link = article.find('h3', class_='title').find('a')['href']
            data.append({
                'Title': title,
                'Link': urljoin(base_url, link),
                'Time': item_time
            })
    return data


def crawl_links(last_time=None):
    # Main logic to go through each page
    data_all = []
    web_url = 'https://vietnambiz.vn/doanh-nghiep.htm'
    # do not go over 550
    for page in range(1, 549):  # Adjust this range according to the number of pages you want to scrape
        print("Page", page)
        if page > 1:
            web_url = f'https://vietnambiz.vn/doanh-nghiep/trang-{page}.htm'
        if last_time:
            data_all.extend(parse_html(web_url, last_time))
        else:
            data_all.extend(parse_html(web_url))
    return data_all


def crawl_items():
    # Load existing data
    if os.path.exists('./data/links/news_link_vietnambiz.json'):
        print("---- Continue ----")
        with open('./data/links/news_link_vietnambiz.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            last_time = existing_data[-1]["Time"]
            existing_data.extend(crawl_links(last_time))
    else:
        existing_data = []
        existing_data.extend(crawl_links())

    print("Total:", len(existing_data))
    # Save the data to a JSON file
    with open('./data/links/news_link_vietnambiz.json', 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)


crawl_items()
