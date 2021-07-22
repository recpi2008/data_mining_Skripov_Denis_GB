import requests
from pprint import pprint

def get_extention(headers):
    if 'Content-Type' not in headers:
        raise ValueError("There are no Content-Type")
    return headers['Content-Type'].split('/')[-1]

headers = { "USER_AGENT": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
           ' (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}
url = "https://images.ru.prom.st/644119431_gobelenovaya-kartina-.jpg"
response = requests.get(url,headers=headers)

exception = get_extention(response.headers)
with open(f"images.{exception}", "wb") as f:
    f.write(response.content)