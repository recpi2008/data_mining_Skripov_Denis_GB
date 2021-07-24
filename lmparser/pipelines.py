# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from pymongo import MongoClient
import hashlib
from scrapy.utils.python import to_bytes

file_dir = ''

def list_to_dict(characteristics_list):
    def_list_new = {}
    for i in range(len(characteristics_list)//2):
        i *= 2
        def_list_new[characteristics_list[i]] = characteristics_list[i+1]
    return def_list_new


class LmparserPipeline:
    def __init__(self):
        client  = MongoClient('localhost',27017)
        self.mongo_base = client.leroymerlin

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item["characteristics_list"]=list_to_dict(item["characteristics_list"])
        # print(1)
        if len(list(collection.find({"url": item["url"]}))) < 1:
            collection.insert_one(item)
        return item

class LmPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)
    def file_path(self, request, response=None, info=None,*,item=None):
        file_dir = item["name"][0]
        image_id = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f"{file_dir}/{image_id}.jpg"


    def item_completed(self, results, item, info):
        if results:
            item['photos']= [itm[1] for itm in results if itm[0]]
        return item



