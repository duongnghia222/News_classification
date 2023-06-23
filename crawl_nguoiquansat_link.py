from bs4 import BeautifulSoup  # Import thư viện BeautifulSoup để phân tích HTML
import requests  # Import thư viện requests để tải nội dung HTML từ URL
import json  # Import thư viện json để làm việc với dữ liệu JSON
from urllib.parse import urljoin  # Import hàm urljoin để kết hợp URL tương đối với URL cơ sở
import os  # Import thư viện os để làm việc với tệp và thư mục
from datetime import datetime  # Import thư viện datetime để làm việc với thời gian
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

# Function để phân tích HTML và trích xuất dữ liệu mong muốn
# def parse_html(url):
#     """
#     Hàm này nhận đầu vào là URL của trang web cần phân tích và một tham số from_time để chỉ định thời gian cần lấy bài viết từ.
#     """

#     # Chuyển đổi thời gian từ chuỗi thành đối tượng datetime

#     # Tải nội dung HTML từ URL
#     response = requests.get(url)

#     # Phân tích HTML bằng BeautifulSoup
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Khởi tạo danh sách để lưu trữ dữ liệu
#     data = []

#     # URL cơ sở của trang web
#     base_url = 'https://nguoiquansat.vn/'

#     # Tìm các phần tử div có class 'list-news'
#     list_news_divs = soup.find_all('div', class_='c-template-list is-large-pc')

#     # Lặp qua các phần tử 'list-news' để tìm các phần tử 'item'
#     for list_news_div in list_news_divs:
#         articles = list_news_div.find_all('div', class_='b-grid')

#         # Lặp qua các phần tử 'item' để trích xuất thông tin
#         for article in articles:
#             # Lấy thời gian bài viết và chuyển đổi thành đối tượng datetime
#             # item_time = article.find('span', class_='timeago need-get-timeago').get_text(strip=True)
#             # article_time = datetime.strptime(item_time, '%H:%M | %d/%m/%Y')

#             # # Kiểm tra nếu thời gian bài viết lớn hơn hoặc bằng thời gian from_time, bỏ qua và chuyển đến bài viết tiếp theo
#             # if article_time >= from_time:
#             #     continue

#             # Trích xuất tiêu đề và liên kết của bài viết
#             title = article.find('h3', class_='b-grid__title').text.strip()
#             link = article.find('h3', class_='b-grid__title').find('a')['href']

#             # Thêm dữ liệu vào danh sách
#             data.append({
#                 'Title': title,
#                 'Link': urljoin(base_url, link),
#             })

#     # Trả về dữ liệu
#     return data


# Hàm chính để thu thập các liên kết từ các trang web
def crawl_links(last_time=None):
    """
    Hàm này điều khiển quá trình thu thập dữ liệu từ các trang web.
    """
    base_url = 'https://nguoiquansat.vn/'
    # Khởi tạo danh sách để lưu trữ dữ liệu từ tất cả các trang
    data_all = []

    # URL của trang web

    # Lặp qua từng trang
    # for page in range(1, 11):
    #     print("Page", page)

    #     # Xây dựng URL cho từng trang
    #     if page > 1:
    #         web_url = f'https://vietnambiz.vn/doanh-nghiep/trang-{page}.htm'

    #     # Kiểm tra last_time và gọi hàm parse_html để lấy dữ liệu từ trang
    #     if last_time:
    #         data_all.extend(parse_html(web_url, last_time))
    #     else:
    #         data_all.extend(parse_html(web_url))
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
        driver.implicitly_wait(10)

        # Lấy nội dung mới đã tải và sử dụng BeautifulSoup để phân tích cú pháp HTML
        
            
        a+=1
        if a>=100:
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
    if os.path.exists('link_nguoiquansat.json'):
        print("---- Continue ----")
        with open('link_nguoiquansat.json', 'r', encoding='utf-8') as f:
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
    with open('link_nguoiquansat.json', 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)


crawl_items()
