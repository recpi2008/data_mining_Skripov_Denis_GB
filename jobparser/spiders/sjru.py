import scrapy
from scrapy.http import HtmlResponse # подсказка для response
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&noGeo=1']

    def parse(self, response:HtmlResponse):
        links = response.xpath("//a[contains(@class,'icMQ_ _6AfZ9 f-test-link-')]/@href").extract()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)
        next_page = response.xpath("//a[contains(@class,'f-test-link-Dalshe')]/@href").extract_first()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        vacancy_name = response.xpath("//h1//text()").extract_first()
        vacancy_salary = response.xpath("//span[@class='_1OuF_ ZON4b']//text()").extract()
        vacancy_url = response.url
        vacancy_sourse = 'superjob.ru'

        yield JobparserItem(name=vacancy_name, salary=vacancy_salary, url=vacancy_url, sourse=vacancy_sourse)
