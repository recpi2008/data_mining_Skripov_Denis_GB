# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramScraperItem(scrapy.Item):
    _id = scrapy.Field()
    user = scrapy.Field()
    user_name = scrapy.Field()
    user_photo = scrapy.Field()
    user_stutus = scrapy.Field()
    # user_id = scrapy.Field()
    # id = scrapy.Field()
    # metadata = scrapy.Field()