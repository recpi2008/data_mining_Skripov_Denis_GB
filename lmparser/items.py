# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def price_int(value):
    if value:
        value = int(value.replace(" ", ''))
    return value


def process_url(value):
    if value:
        value = value.replace('w_82,h_82', 'w_1200,h_1200')
    return value


def process_charact(value):
    if value:
        value = value.replace(' ', '').replace('\n', '')
    return value


class LmparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(price_int))
    photos = scrapy.Field(input_processor=MapCompose(process_url))
    url = scrapy.Field()
    characteristics_list = scrapy.Field(input_processor=MapCompose(process_charact))
    _id = scrapy.Field()
