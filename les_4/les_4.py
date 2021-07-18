import requests
from lxml import html
from pprint import pprint
from pymongo import MongoClient
from time import sleep

class Newslenta:
    def __init__(self, start_url, headers, db_client):
        self.start_url = start_url
        self.start_headers = headers
        self.db = db_client['basa_news']
        self.news = self.db.news
        # self.info_news=[]


    def get_html_string(self, url, headers):
        try:
            response = requests.get(url, headers=headers)
            if response.ok:
                return response.text

        except Exception as e:
            sleep(1)
            print(e)
            return None

    @staticmethod
    def get_dom(html_string):
        return html.fromstring(html_string)

    def run(self):
        html_string = self.get_html_string(self.start_url, self.start_headers)
        dom_lenta = html.fromstring(html_string)
        items_lenta = dom_lenta.xpath('//div[contains(@class,"b-yellow-box__wrap")]//div[contains(@class,"item")]')
        self.get_info_from_element(items_lenta)
        # self.save_in_mongo()


    def get_info_from_element(self, items_lenta):
        for item in items_lenta:
            lenta_item = {}

            name_news = item.xpath(".//a/text()")[0].replace('\xa0', ' ')
            lenta_item["name_news"] = name_news

            link_news = main_url_lenta + item.xpath(".//a/@href")[0]
            lenta_item["link_news"] = link_news
            lenta_item["source_news"] = main_url_lenta

            response_data = requests.get(link_news, headers=headers)
            dom_lenta_data = html.fromstring(response_data.text)

            data_lenta = dom_lenta_data.xpath('.//time[@class="g-date"]/text()')

            lenta_item["data_news"] = "".join(data_lenta)
            self.save_without_repeat(lenta_item)
            # self.info_news.append(lenta_item)

    def save_without_repeat(self, lenta_item):
        if len(list(self.news.find({"link_news": lenta_item["link_news"]}))) < 1:
            self.news.insert_one(lenta_item)

    # def save_in_mongo(self):
    #     self.news.insert_many(self.info_news)


class Newsyandex:
    def __init__(self, start_url, headers, db_client):
        self.start_url = start_url
        self.start_headers = headers
        self.db = db_client['basa_news']
        self.news = self.db.news
        # self.info_news=[]

    def get_html_string(self, url, headers):
        try:
            response = requests.get(url, headers=headers)
            if response.ok:
                return response.text

        except Exception as e:
            sleep(1)
            print(e)
            return None

    @staticmethod
    def get_dom(html_string):
        return html.fromstring(html_string)


    def run(self):
        html_string = self.get_html_string(self.start_url, self.start_headers)
        dom_yandex = html.fromstring(html_string)
        items_yandex = dom_yandex.xpath('//div[@class="mg-grid__row mg-grid__row_gap_8 news-top-flexible-stories news-app__top"]//div[contains(@class,"mg-grid__col")]')
        self.get_info_from_element(items_yandex)
        # self.save_in_mongo()

    def get_info_from_element(self, items_yandex):
        for item in items_yandex:
            yandex_item = {}

            name_yandex = item.xpath('.//h2[@class="mg-card__title"]/text()')[0].replace('\xa0', ' ')
            link_yandex = item.xpath(".//a/@href")[0]
            source_yandex = item.xpath(".//a[@class='mg-card__source-link']/text()")
            time_yandex = item.xpath('.//span[@class="mg-card-source__time"]/text()')
            main_url_yandex = item.xpath(".//a[@class='mg-card__source-link']/text()")

            yandex_item["text_news"] = name_yandex
            yandex_item["link_news"] = link_yandex
            yandex_item["source_news"] = ''.join(source_yandex)
            yandex_item["data_news"] = ''.join(time_yandex)

            self.save_without_repeat(yandex_item)

            # self.info_news.append(yandex_item)

    def save_without_repeat(self, yandex_item):
        if len(list(self.news.find({"link_news": yandex_item["link_news"]}))) < 1:
            self.news.insert_one(yandex_item)

    # def save_in_mongo(self):
    #     self.news.insert_many(self.info_news)


class Newsmail:
    def __init__(self, start_url, headers, db_client):
        self.start_url = start_url
        self.start_headers = headers
        self.db = db_client['basa_news']
        self.news = self.db.news
        # self.info_news=[]

    def get_html_string(self, url, headers):
        try:
            response = requests.get(url, headers=headers)
            if response.ok:
                return response.text

        except Exception as e:
            sleep(1)
            print(e)
            return None

    @staticmethod
    def get_dom(html_string):
        return html.fromstring(html_string)

    def run(self):
        html_string = self.get_html_string(self.start_url, self.start_headers)
        dom_mail = html.fromstring(html_string)
        items_mail = dom_mail.xpath("//div[@class='block']")
        self.get_info_from_element(items_mail)
        # self.save_in_mongo()

    def get_info_from_element(self, items_mail):
        for item in items_mail:
            link_mail = list(set(item.xpath('.//a/@href')))

        for item_l in link_mail:
            response = requests.get(item_l, headers=headers)
            dom_mail = html.fromstring(response.text)
            items_mail = dom_mail.xpath("//div[@class='block']")

            mail_item = {}
            mail_item["link_news"] = item_l

            for item in items_mail:
                name_mail = item.xpath('//h1/text()')
                source_mail = item.xpath("//a[@class='link color_gray breadcrumbs__link']//text()")
                time_mail = item.xpath("//span[@class='note__text breadcrumbs__text js-ago']//text()")

                mail_item["name_news"] = ''.join(name_mail)
                mail_item["source_news"] = ''.join(source_mail)
                mail_item["data_news"] = ''.join(time_mail)
                # self.info_news.append(mail_item)
                self.save_without_repeat(mail_item)

    def save_without_repeat(self, mail_item):
        if len(list(self.news.find({"link_news": mail_item["link_news"]}))) < 1:
            self.news.insert_one(mail_item)

    # def save_in_mongo(self):
    #     self.news.insert_many(self.info_news)


if __name__ == '__main__':

    db_client = MongoClient('localhost', 27017)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}

    main_url_lenta = "https://lenta.ru/"
    scraper_lenta = Newslenta(main_url_lenta, headers, db_client)
    scraper_lenta.run()

    main_url_yandex = "https://yandex.ru/news"
    scraper_yandex = Newsyandex(main_url_yandex, headers, db_client)
    scraper_yandex.run()

    main_url_mail = "https://news.mail.ru/"
    scraper_mail = Newsmail(main_url_mail, headers, db_client)
    scraper_mail.run()












