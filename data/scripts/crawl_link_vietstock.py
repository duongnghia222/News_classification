import os
import json
import sys
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

NUMBER_OF_PAGES_CRAWL = 380

WEBDRIVER_DELAY_TIME_INT = 5
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')

driver = webdriver.Chrome('chromedriver', options=chrome_options)

driver.implicitly_wait(3)
wait = WebDriverWait(driver, WEBDRIVER_DELAY_TIME_INT)

main_url = "https://vietstock.vn/doanh-nghiep.htm"
driver.get(main_url)

content_tags_xpath = '//*[@id="channel-container"]/div[@class="single_post post_type12 type20 mb20 channelContent"]'
content_tags = driver.find_elements(By.XPATH, content_tags_xpath)

result = []

for _ in tqdm(range(NUMBER_OF_PAGES_CRAWL)):
    print(len(content_tags))
    for idx in tqdm(range(len(content_tags))):
        content_title_xpath = f'//*[@id="channel-container"]/div[{1+3*idx}]/div[2]/h4/a'
        meta_xpath = f'//*[@id="channel-container"]/div[{1+3*idx}]/div[2]/div[1]/div/div/a'
        try:
            news_title = wait.until(EC.presence_of_element_located((By.XPATH, content_title_xpath))).get_attribute('title')
            news_url = wait.until(EC.presence_of_element_located((By.XPATH, content_title_xpath))).get_attribute('href')
            news_type = wait.until(EC.presence_of_element_located((By.XPATH, meta_xpath + '[1]'))).get_attribute('title')
            news_published_time = wait.until(EC.presence_of_element_located((By.XPATH, meta_xpath + '[2]'))).get_attribute('title')
            # print(news_title)
            dictionary = {
                'title': news_title,
                'link': news_url,
                'time': news_published_time,
                'type': news_type
            }
            result.append(dictionary)
        except:
            pass
    button = driver.find_element(By.XPATH, '//*[@id="page-next "]/a')
    driver.execute_script("arguments[0].click()", button)

print(result)

if os.path.exists('./data/contents/news_links_vietstock.json'):
    os.remove('./data/contents/news_links_vietstock.json')
import json
with open('./data/contents/news_links_vietstock.json', 'w+', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
