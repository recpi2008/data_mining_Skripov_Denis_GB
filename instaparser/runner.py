import os

from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instaparser import settings
from instaparser.spiders.instagram import InstagramSpider

if __name__ == "__main__":
    load_dotenv(r"C:\Users\ivane\eles\data_mining_Skripov_Denis_GB\instaparser\.env_inst.py")
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")
    # user_to_parse = os.getenv("USER_TO_PARSE")
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    user_to_parse = input("Введите, пользователей:\n").split(' ')

    process = CrawlerProcess(settings=crawler_settings)
    kwargs = {
        "login": login,
        "password": password,
        "user_to_parse": user_to_parse,
    }
    process.crawl(InstagramSpider, **kwargs)

    process.start()