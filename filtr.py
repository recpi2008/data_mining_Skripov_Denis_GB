from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['instagram']
instagram = db.instagram


def following():
    user = input("Введите пользавателя:")
    result = instagram.find({'$and': [{"user": user}, {'user_stutus': 'following'}]},{'user': False,'user_stutus':False,'_id': False})
    for user in result:
        pprint(user)

def follower():
    user = input("Введите пользавателя:")
    result = instagram.find({'$and': [{"user": user}, {'user_stutus': 'follower'}]},{'user': False,'user_stutus':False,'_id': False})
    for user in result:
        pprint(user)

if __name__ == '__main__':
    following()
    follower()