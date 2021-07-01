"""
Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json; написать функцию, возвращающую список репозиториев.
"""

import json
from pprint import pprint
import requests


# Неаутентифицированные клиенты могут делать 60 запросов в час.

def get_response(user_name):
    """Получаем response"""
    url = f"https://api.github.com/users/{user_name}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        return response
    return None


def save_json(response_get):
    """Сохраняем json"""
    with open("repos_list.json", "w") as f:
        json.dump(response_get.json(), f)


def repos_list(response_join):
    """Возвращаем список репозиториев"""
    user_list = []
    for i in response_join.json():
        user_list.append(i["name"])
    return user_list

def pipeline_repos():
    # username = input()
    username = "recpi2008"
    response = get_response(username)
    save_json(response)
    repos_lists = repos_list(response)
    pprint(repos_lists)

if __name__ == "__main__":
    pipeline_repos()



