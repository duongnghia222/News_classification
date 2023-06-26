# Installation
Download Chormedriver at `https://chromedriver.chromium.org/downloads`

pip install beautifulsoup4

pip install selenium

|-- data
|   |-- tickers
|       |-- hnx_tickers.csv
|       |-- hose_tickers.csv
|       |-- uc_tickers.csv
|   |-- content
|       |-- news_data_vietstock.json
|       |-- news_link_vietstock.json
|       |-- news_data_vietnambiz.json
|       |-- news_link_vietnambiz.json
|       |-- news_data_nguoiquansat.json
|       |-- news_link_nguoiquansat.json
|   |-- scripts
|       |-- crawl_data_vietstock.py    # ---export---> news_data_vietstock.json
|       |-- crawl_link_vietstock.py    # ---export---> news_link_vietstock.json
|       |-- crawl_data_vietnambiz.py   # ---export---> news_data_vietnambiz.json
|       |-- crawl_link_vietnambiz.py   # ---export---> news_link_vietnambiz.json
|       |-- crawl_data_nguoiquansat.py # ---export---> news_data_nguoiquansat.json
|       |-- crawl_link_nguoiquansat.py # ---export---> news_link_nguoiquansat.json 
|-- models
|   |--
|-- configs
|-- weights
|-- utils
    |-- split_json.py
|-- auto_label.py
|-- infer.py
|-- requirements.txt
|-- README.md