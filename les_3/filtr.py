from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['basa_job_sj_hh']
jobs = db.jobs

# сортировка
pay_from = int(input("Введите сумму:"))
result = jobs.find({'макс зарплата':{'$gt':pay_from}},{'вакансия':True, 'кампания': True,'ссылка на вакансию':True, 'макс зарплата':True, '_id':False}) # '$gt' значит > , '$lt' значит <, '$gte'

for user in result:
    pprint(user)

# только новые вакансии с сайта, можно через upsert=True
# def value_unique(our_dict):
#     for vacancy_new in our_dict:
#         jobs.update(vacancy, vacancy_new, upsert=True)

