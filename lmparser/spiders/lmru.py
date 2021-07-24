import scrapy
from scrapy.http import HtmlResponse
from lmparser.items import LmparserItem
from scrapy.loader import ItemLoader


class LmruSpider(scrapy.Spider):
    name = 'lmru'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['http://leroymerlin.ru/']

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        url = f"https://leroymerlin.ru/search/?q={query}&suggest=true&fromRegion=34"
        self.start_urls = [url]

    def parse(self, response:HtmlResponse):
        links = response.xpath('//a[@data-qa="product-name"]')
        for link in links:
            yield response.follow(link, callback=self.parse_item)
        next_page = response.xpath('//a[@data-qa-pagination-item="right"]/@href').extract_first()
        if next_page:
            # print(1)
            yield response.follow(next_page, callback=self.parse)

    def parse_item(self, response: HtmlResponse):
        loader = ItemLoader(item=LmparserItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price','//span[@slot="price"]/text()')
        loader.add_xpath('photos', '//img[@slot="thumbs"]/@src')
        loader.add_value('url', response.url)
        loader.add_xpath('characteristics_list',
                         '//dt[@class="def-list__term"]/text()' + '|' + '//dd[@class="def-list__definition"]/text()')

        yield loader.load_item()
