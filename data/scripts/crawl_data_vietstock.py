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

def crawl_text_and_tags(url, title= None):
    driver.get(url)
    information_xpath = '//*[@id="vst_detail"]/p'
    news_content = ""
    news_tags = []
    
    # Get content from url
    try: 
        information = wait.until(EC.presence_of_all_elements_located((By.XPATH, information_xpath)))
        for i in range(len(information)):
            if information[i].get_attribute('class') not in ["pTitle", "pAuthor", "pSource"]:
                if news_content:
                    news_content += ' '
                news_content += information[i].text
        print("SUCCESS - content")
    except:
        print("FAULT - content")
        if title:
            print(f"FAULT - {title}")
    
    # Get tags from url
    try:
        # tags = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tags mt20')))
        print("1")
        tags = driver.find_elements(By.XPATH, '//*[@class="tags mt20"]/ul/li')
        # tags = wait.until(EC.presence_of_all_elements_located((By.XPATH, f'//*[@id="article-{url[-11:-4]}"]/div[1]/div[2]/div[2]/div[3]/ul/li')))
        print("2", len(tags))
        for idx in range(len(tags)):
            if tags[idx].get_attribute('class') == 'tag_list':
                print("Not append")
            else:
                news_tags.append(tags[idx].text)
    except:
        print("FAULT - tags")

    return news_content, news_tags
# url = 'https://vietstock.vn/2023/06/dhdcd-qcg-muc-tieu-doanh-thu-8211-loi-nhuan-2023-trai-chieu-doi-ngay-tra-co-tuc-2021-den-quy-32025-737-1081685.htm'
# print(url[-11:-4])
# //*[@id="article-1081685"]/div[1]/div[2]/div[2]/div[3]/ul
with open('./data/contents/news_links_vietstock.json', 'r', encoding='utf-8') as f:
    data =json.load(f)

result = []
for idx in tqdm(range(len(data))):
    main_content, tags = crawl_text_and_tags(data[idx]['link'])
    dictionary = {
        'title': data[idx]['title'],
        'content': main_content,
        'tags': tags
    }
    result.append(dictionary)
    if idx == 2: break
print(result)