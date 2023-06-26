from bs4 import BeautifulSoup  # Import thư viện BeautifulSoup để phân tích HTML
import requests  # Import thư viện requests để tải nội dung HTML từ URL
import json  # Import thư viện json để làm việc với dữ liệu JSON
from urllib.parse import urljoin  # Import hàm urljoin để kết hợp URL tương đối với URL cơ sở
import os  # Import thư viện os để làm việc với tệp và thư mục
import time
from datetime import datetime  # Import thư viện datetime để làm việc với thời gian
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

# Hàm chính để thu thập các liên kết từ các trang web
def crawl_links(last_time=None):
    """
    Hàm này điều khiển quá trình thu thập dữ liệu từ các trang web.
    """
    base_url = 'https://nguoiquansat.vn/'
    # Khởi tạo danh sách để lưu trữ dữ liệu từ tất cả các trang
    data_all = []

    a=0
    driver = webdriver.Chrome()
    driver.get("https://nguoiquansat.vn/chung-khoan")
    while True:
        
        
        try:
            view_more_button = driver.find_element("xpath","//a[@href='javascript:;']")
            actions = ActionChains(driver)
            actions.move_to_element(view_more_button).click().perform()
        except:
            print("")

        # Chờ trang web tải thêm nội dung
        # driver.implicitly_wait(10)
        time.sleep(1)

        # Lấy nội dung mới đã tải và sử dụng BeautifulSoup để phân tích cú pháp HTML
        
        print(f"Clicked : {a}")
        a+=1
        if a>=300:
            break
        
    new_content = driver.find_element("xpath","//div[@class='c-template-list is-large-pc']")
        #print(new_content.get_attribute('innerHTML'))
    soup = BeautifulSoup(new_content.get_attribute('innerHTML'), 'html.parser')
    
    articles = soup.find_all('div', class_='b-grid')
    
    data = []
    
    for article in articles:
        
        title = article.find('h3', class_='b-grid__title').text.strip()
        link = article.find('h3', class_='b-grid__title').find('a')['href']

        # Thêm dữ liệu vào danh sách
        data.append({
            'Title': title,
            'Link': urljoin(base_url, link),
        })
        
    data_all.extend(data)
        
        


    # Trả về dữ liệu từ tất cả các trang
    return data_all


# Hàm chính để điều khiển quá trình thu thập dữ liệu
def crawl_items():
    """
    Hàm này điều khiển quá trình thu thập dữ liệu từ trang web và lưu dữ liệu vào tệp JSON.
    """

    # Kiểm tra xem tệp JSON đã tồn tại chưa
    if os.path.exists('./data/links/news_link_nguoiquansat.json'):
        print("---- Continue ----")
        with open('./data/links/news_link_nguoiquansat.json', 'r', encoding='utf-8') as f:
            # Nếu tệp đã tồn tại, tải dữ liệu từ tệp và lấy thời gian cuối cùng để truyền vào crawl_links
            existing_data = json.load(f)
            #last_time = existing_data[-1]["Time"]
            existing_data.extend(crawl_links())
    else:
        # Nếu tệp không tồn tại, khởi tạo danh sách rỗng và gọi crawl_links để lấy dữ liệu
        existing_data = []
        existing_data.extend(crawl_links())

    print("Total:", len(existing_data))
    #print(existing_data)

    # Lưu dữ liệu vào tệp JSON
    with open('./data/links/news_link_nguoiquansat.json', 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)


crawl_items()
