from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json
import os
from urllib.parse import urljoin


# Function to parse articles
def parse_articles(soup):
    base_url = 'https://www.tinnhanhchungkhoan.vn'
    data = []
    category_timeline_div = soup.find('div', class_='category-timeline')
    if not category_timeline_div:
        print("can not find category_timeline_div")
        return data
    articles = category_timeline_div.find_all('article', class_='story')
    for article in articles:
        title_tag = article.find('h2', class_='story__heading') or article.find('h3', class_='story__heading')
        title = title_tag.get_text(strip=True) if title_tag else 'N/A'
        link_tag = article.find('a', class_='cms-link')
        if link_tag:
            link = link_tag['href']
            if not link.startswith(base_url):
                link = urljoin(base_url, link)
        else:
            link = 'N/A'
        time_tag = article.find('time')
        time_ = time_tag.get_text(strip=True) if time_tag else 'N/A'
        data.append({'Title': title, 'Link': link, 'Time': time_})
    return data


def create_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # headless mode
    # Set path to chromedriver as per your configuration
    service = Service(executable_path='C:/Program Files (x86)/chrome_driver/chromedriver')
    # Create Chrome WebDriver
    driver = webdriver.Chrome(chrome_options, service)
    return driver


def crawl_news():
    # Navigate to the page
    driver = create_driver()
    driver.get('https://www.tinnhanhchungkhoan.vn/doanh-nghiep/')

    # Wait some seconds for page to load completely
    time.sleep(2)

    # Get the initial articles on the page
    initial_soup = BeautifulSoup(driver.page_source, 'html.parser')
    new_data = parse_articles(initial_soup)

    # For first n pages
    for _ in range(2):
        # Find the "Xem them" button and click it
        button = driver.find_element(By.CLASS_NAME, "control__loadmore")
        button.click()

        # Wait for the content to load
        time.sleep(5)

        # Get the loaded articles on the page
        loaded_soup = BeautifulSoup(driver.page_source, 'html.parser')
        new_data.extend(parse_articles(loaded_soup))

    # Close the driver
    driver.quit()

    # Load existing data
    if os.path.exists('news_links.json'):
        with open('news_links.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    # Check new data against existing data
    for item in new_data:
        if item not in existing_data:
            existing_data.append(item)

    # Save the data to a JSON file
    with open('news_links.json', 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)


crawl_news()
