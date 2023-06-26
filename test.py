from bs4 import BeautifulSoup
import requests
import json
import os

import requests

HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

url = 'https://vietstock.vn/2023/06/dhdcd-mpc-kinh-doanh-co-the-tot-len-tu-thang-8-nghien-cuu-cac-mo-hinh-nuoi-tom-737-1081687.htm'
req = requests.get(url, headers= HEADERS)
print(req.status_code)
print(req.text)
output = []
print(len(output))