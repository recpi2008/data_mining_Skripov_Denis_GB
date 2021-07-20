# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy2021


    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        if item['sourse'] == 'superjob.ru':
            salary_min, salary_max, currency = self.process_salary_sj(item['salary'])
            item['min_salary'] = salary_min
            item['max_salary'] = salary_max
            item['currency'] = currency
        elif item['sourse'] == 'hh.ru':
            salary_min, salary_max, currency = self.process_salary_hh(item['salary'])
            item['min_salary'] = salary_min
            item['max_salary'] = salary_max
            item['currency'] = currency


        del item['salary']
        collection.insert_one(item)

        return item

    def process_salary_hh(self, salary):
        salary = salary[0].replace('\xa0', '').split(' ')
        if 'от' in salary:
            if 'до' in salary:
                salary_min = float(salary[1])
                salary_max = float(salary[-2])
                currency = salary[-1]
                return salary_min, salary_max, currency

            else:
                salary_min = float(salary[1])
                salary_max = None
                currency = salary[-1]
                return salary_min, salary_max, currency

        elif 'з/п' in salary:
            salary_min = None
            salary_max = None
            currency = None
            return salary_min, salary_max, currency

        elif 'до' in salary:
            salary_min = None
            salary_max = float(salary[-2])
            currency = salary[-1]
            return salary_min, salary_max, currency

    def process_salary_sj(self, salary):
        if 'По' in salary:
            salary_min = None
            salary_max = None
            currency = None
            return salary_min, salary_max, currency
        elif 'от' in salary:
            salary = salary[2].split('\xa0')
            currency = salary.pop()
            salary_min = float(''.join(salary))
            salary_max = None
            return salary_min, salary_max, currency
        elif '—' in salary:
            salary = [salary[0].replace('\xa0',''), salary[4].replace('\xa0',''), salary[6]]
            salary_min = float(salary[0])
            salary_max = float(salary[1])
            currency = salary[-1]
            return salary_min, salary_max, currency
        elif 'до' in salary:
            salary = salary[2].split('\xa0')
            currency = salary.pop()
            salary_min = None
            salary_max = float(''.join(salary))
            return salary_min, salary_max, currency
