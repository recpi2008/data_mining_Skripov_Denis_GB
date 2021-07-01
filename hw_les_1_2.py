"""
Зарегистрироваться на https://openweathermap.org/api и написать функцию, которая получает погоду в данный
момент для города, название которого получается через input. https://openweathermap.org/current
"""
import os
from pprint import pprint

import requests
from dotenv import load_dotenv

# относительный путь для примера, лучше использовать глобальный!
load_dotenv("./.env")

key = "API_OW"
open_key = os.getenv(key, None)


def get_response(city, api_key):
    """ "Получаем response"""
    try:
        main_link = "http://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": api_key}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
            "Accept": "*/*",
        }
        response = requests.get(main_link, params=params, headers=headers)
        j_body = response.json()
        return j_body
    except Exception as e:
        return None


def info_weather(j_body):
    """Выводим нужные параметры"""
    return pprint(
        f"В городе {j_body.get('name')} температура {round(j_body.get('main').get('temp') - 273)} градусов"
    )


def pipeline():
    user_city = input()
    try:
        j_body = get_response(user_city, open_key)
        return info_weather(j_body)
    except Exception as e:
        print("Не коректный ввод")


if __name__ == "__main__":
    pipeline()
