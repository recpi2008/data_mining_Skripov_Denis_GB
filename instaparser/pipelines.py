# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from pymongo import MongoClient

class InstagramScraperPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.instagram


    def process_item(self, item, spider):
        follow = self.mongo_base[spider.name]
        # if len(list(follow.find({"user_name": item["user_name"]} and {"user_stutus": item["user_stutus"]}))) < 1:
        follow.insert_one(item)
        return item