from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lmparser.spiders.lmru import LmruSpider
from lmparser import settings

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    # query = quote_plus("обои".encode(encoding="cp1251"))

    # query = input("Введите, что ищем:\n")
    query = "ковер"

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LmruSpider, query=query)

    process.start()

