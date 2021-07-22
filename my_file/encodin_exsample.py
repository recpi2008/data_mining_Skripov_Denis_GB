import requests
from urllib.parse import quote_plus
from pprint import pprint

headers = { "USER_AGENT": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
           ' (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}

# querty = "материнские платы asus"
#
# url = f"https://www.onlinetrade.ru/sitesearch.html?query={querty}"
# response = requests.get(url, headers=headers)
# print(1)
querty = quote_plus("материнские платы asus".encode(encoding='cp1251'))

url = f"https://www.onlinetrade.ru/sitesearch.html?query={querty}"
response = requests.get(url, headers=headers)
print(1)