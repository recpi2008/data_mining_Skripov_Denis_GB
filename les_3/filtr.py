from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['basa_job_sj_hh']
jobs = db.jobs

# сортировка
def pay_from():
    pay_user = int(input("Введите сумму:"))
    # result = jobs.find({'макс зарплата':{'$gt':pay_user}},{'вакансия':True, 'кампания': True,'ссылка на вакансию':True, 'макс зарплата':True, '_id':False}) # '$gt' значит > , '$lt' значит <, '$gte'
    result = jobs.find({'$or':[{'мин зарплата':{'$gt':pay_user}},{'макс зарплата':{'$gt':pay_user}}]})
    for user in result:
        pprint(user)

if __name__ == '__main__':
    pay_from()


