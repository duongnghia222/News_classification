import os
import json
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

WEBDRIVER_DELAY_TIME_INT = 5
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')

driver = webdriver.Chrome('chromedriver', options=chrome_options)

driver.implicitly_wait(4)
wait = WebDriverWait(driver, WEBDRIVER_DELAY_TIME_INT)

def crawl_text(url, title= None):
    driver.get(url)
    information_xpath = '//*[@id="vst_detail"]/p'
    # contents = driver.find_elements(By.XPATH, content_xpath)
    try: 
        information = wait.until(EC.presence_of_all_elements_located((By.XPATH, information_xpath)))
        news_content = ""
        for i in range(len(information)):
            if information[i].get_attribute('class') not in ["pTitle", "pAuthor", "pSource"]:
                if news_content:
                    news_content += ' '
                news_content += information[i].text
        return news_content
    except:
        if title:
            print(f"FAULT - {title}")
        return "", ""


with open('./../contents/news_links_vietstock.json', 'r', encoding='utf-8') as f:
    data =json.load(f)

result = []
for idx in tqdm(range(data)):
    main_content, tags = crawl_text(data[idx]['link'])
    dictionary = {
        'title': data[idx]['title'],
        'content': main_content,
        'tags': tags
    }

