from bs4 import BeautifulSoup
import requests
import json
import os

import requests
#
# HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
#
# url = 'https://vietstock.vn/2023/06/dhdcd-mpc-kinh-doanh-co-the-tot-len-tu-thang-8-nghien-cuu-cac-mo-hinh-nuoi-tom-737-1081687.htm'
# req = requests.get(url, headers= HEADERS)
# print(req.status_code)
# print(req.text)
# output = []
# print(len(output))
#
# '''
#     data = {
#         'content': content,
#         'label': Mã chứng khoán (Ticker)
#     }
# '''

import requests

url = 'https://storage.googleapis.com/kagglesdsdata/datasets/900644/1527621/vietnamese.txt?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20230703%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230703T103953Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=1bfab0a821562c3471beb15ee20aed24adc1a99223d6777a3dcb49a23f0ba48e6fa367cc9a47f460aa1871b133647b1ea996d35d455c163af3e643811b4babaa8dba121ff02fdc757c18d961aea314fa6aed73590f766dee9a59b309b412fea36ffa6e89fa3cc8d450c2f7b422a7c362686e866dcbbce4ead8afdea29033225dace0f8c6ce19fca500c199de414873a5f3c8d697222e568a622301a77a221ab416e60fb854285b3c346bf2f04a3597b89ca9537d4263bf551d0ae8ca2a20d20e4b6f233b25240a5c78ee4711ccfa4c43468561c7f89e30323cdc2cc9a9c8d619b431081aa185c91e2e9ee0925e5152d91eca2e21de1245dcc176c109bc86cd9e'
response = requests.get(url)

with open('vietnamese_stopword.txt', 'w', encoding='utf-8') as f:
    f.write(response.text)
