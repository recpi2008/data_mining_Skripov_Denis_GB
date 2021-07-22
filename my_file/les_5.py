import os
from time import sleep
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

load_dotenv()
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

DRAVER_PATH = "../../../Desktop/Скрипов/chromedriver/chromedriver.exe"

url = "https://gb.ru/login"

options = webdriver.ChromeOptions()
options.add_argument("--window-size=500,500")
# options.add_argument("--start-maximized") # на весь экран

driver = webdriver.Chrome(DRAVER_PATH, options=options)
driver.get(url)

user_email = driver.find_element_by_id("user_email")
user_email.send_keys(EMAIL)

user_password = driver.find_element_by_id("user_password")
user_password.send_keys(PASSWORD)
user_password.send_keys(Keys.ENTER)
sleep(3)

url_profile = "https://gb.ru/profile"
driver.get(url_profile)

city = driver.find_element_by_name("user[city]")
city.clear()
sleep(1)
city.send_keys("Москва")

gender = driver.find_element_by_name("user[gender]")
select = Select(gender)

# по индексу для не выбран
# select.select_by_index(0)
# select.select_by_value("female")
sleep(3)
select.select_by_visible_text("Мужской")
gender.submit()
sleep(2)

url = "https://gb.ru/logout"
driver.get(url)


# driver.close() - закрывает вкладку
# driver.quit() - закрывает браузер
sleep(15)
driver.close()


