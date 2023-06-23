from bs4 import BeautifulSoup
import requests
import json
import os

url = 'https://vietstock.vn/2023/06/trs-sap-chia-co-tuc-bang-tien-ty-le-15-738-1079268.htm'
req = requests.get(url)
print(req.status_code)