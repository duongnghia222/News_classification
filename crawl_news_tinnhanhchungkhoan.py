from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json
import os
from urllib.parse import urljoin
from datetime import datetime


# Function to parse articles
def parse_articles(soup, from_time="20/06/2029 20:18"):
    """

    :param soup:
    :param from_time: get article from (from_time : the past)
    :return:
    """
    from_time = datetime.strptime(from_time, '%d/%m/%Y %H:%M')
    base_url = 'https://www.tinnhanhchungkhoan.vn'
    data = []
    category_timeline_div = soup.find('div', class_='category-timeline')
    if not category_timeline_div:
        print("can not find category_timeline_div")
        return data
    articles = category_timeline_div.find_all('article', class_='story')
    for article in articles:
        time_tag = article.find('time')
        time_ = time_tag.get_text(strip=True) if time_tag else 'N/A'
        article_time = datetime.strptime(time_, '%d/%m/%Y %H:%M')
        if article_time >= from_time:
            continue
        title_tag = article.find('h2', class_='story__heading') or article.find('h3', class_='story__heading')
        title = title_tag.get_text(strip=True) if title_tag else 'N/A'
        link_tag = article.find('a', class_='cms-link')
        if link_tag:
            link = link_tag['href']
            if not link.startswith(base_url):
                link = urljoin(base_url, link)
        else:
            link = 'N/A'
        data.append({'Title': title, 'Link': link, 'Time': time_})
    return data


def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # headless mode
    # Set path to chromedriver as per your configuration
    service = Service(executable_path='C:/Program Files (x86)/chrome_driver/chromedriver')
    # Create Chrome WebDriver
    driver = webdriver.Chrome(chrome_options, service)
    return driver


def crawl_links(last_time=None):
    # Navigate to the page
    driver = create_driver()
    driver.get('https://www.tinnhanhchungkhoan.vn/doanh-nghiep/')

    # Wait some seconds for page to load completely
    time.sleep(3)


    new_data = []
    # For first n pages
    for i in range(74):
        print("Page", i + 1, "showed")
        # Find the "Xem them" button and click it
        try:
            button = driver.find_element(By.CLASS_NAME, "control__loadmore")
            button.click()
        except "NoSuchElementException":
            break

        # Wait for the content to load
        time.sleep(3)

    # Get the loaded articles on the page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    if last_time:
        new_data.extend(parse_articles(soup, last_time))
    else:
        new_data.extend(parse_articles(soup))
    print("Total items", len(new_data))

    # Close the driver
    driver.quit()
    return new_data


def crawl_items():
    # Load existing data
    if os.path.exists('news_links_tinnhanhchungkhoan.json'):
        print("---- Continue ----")
        with open('news_links_tinnhanhchungkhoan.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            last_time = existing_data[-1]["Time"]
            existing_data.extend(crawl_links(last_time))
    else:
        existing_data = []
        existing_data.extend(crawl_links())


    print("Total:", len(existing_data))
    # Save the data to a JSON file
    with open('news_links_tinnhanhchungkhoan.json', 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)


crawl_items()
