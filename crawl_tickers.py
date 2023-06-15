import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Uncomment this line to run in headless mode

    # Set path to chromedriver as per your configuration
    service = Service(executable_path='C:/Program Files (x86)/chrome_driver/chromedriver')
    # Create Chrome WebDriver
    driver = webdriver.Chrome(chrome_options, service)
    return driver


def get_data_from_table(soup, url):
    data = []
    if url == "https://www.hsx.vn/Modules/Listed/Web/Symbols?":
        id_ = "symbols-grid"
        table = soup.find("table", {"id": id_})
        for row in table.tbody.find_all("tr")[1:]:
            cols = row.find_all("td")[1:]
            cols = [col.text.strip() for col in cols]
            data.append(cols)

    else:
        id_ = "_tableDatas"
        table = soup.find("table", {"id": id_})
        for row in table.tbody.find_all("tr"):
            cols = row.find_all("td")
            cols = [col.text.strip() for col in cols]
            data.append(cols)
    return data

# Create a function to crawl data
def crawl_data(url, file_name = "file.csv"):
    driver = create_driver()
    driver.get(url)

    # Wait for the page to load
    time.sleep(5)

    # Find the number of pages to crawl
    soup = BeautifulSoup(driver.page_source, "html.parser")

    if url == "https://www.hsx.vn/Modules/Listed/Web/Symbols?":
        num_pages = 14  # hardcode
    else:
        num_pages = int(soup.find("span", {"id": "end"}).parent.get("onclick").split("(")[1].split(")")[0])
    # Initialize data
    data = []

    for page_num in range(1, num_pages + 1):
        print(f"Crawling page {page_num}")
        # Use JavaScript to navigate to the page
        if url == "https://www.hsx.vn/Modules/Listed/Web/Symbols?":
            driver.execute_script(f"$.fn.gridPaging.flip('DbGridPager_1', {page_num}, 14);")
            time.sleep(8)
        else:
            driver.execute_script(f"page({page_num})")
            time.sleep(3)


        # Parse the page source and extract data
        soup = BeautifulSoup(driver.page_source, "html.parser")
        page_data = get_data_from_table(soup, url)
        data.extend(page_data)

    # Close the driver
    driver.quit()

    # Convert the data to a DataFrame
    cols = ["STT", "Stock Code", "Organization Name", "Sector", "First Trading Date", "Listing Volume", "Stock Volume"]
    if url == "https://www.hnx.vn/vi-vn/cophieu-etfs/chung-khoan-uc.html":
        cols.remove("Sector")
    elif url == "https://www.hsx.vn/Modules/Listed/Web/Symbols?":
        cols = ["Stock Code", "ISIN Code", "FIGI Code", "Organization Name", "Listing Volume", "Stock Volume", "First Trading Date"]
    df = pd.DataFrame(data, columns=cols)

    # Save the DataFrame to a CSV file
    df.to_csv(file_name, index=False, encoding="utf-8-sig")

# Start the crawling
file_name = "hose_tickers.csv"  # change name
hnx_link = "https://www.hnx.vn/vi-vn/cophieu-etfs/chung-khoan-ny.html"
uc_link = "https://www.hnx.vn/vi-vn/cophieu-etfs/chung-khoan-uc.html"
hose_link = "https://www.hsx.vn/Modules/Listed/Web/Symbols?"
crawl_data(hose_link, file_name)