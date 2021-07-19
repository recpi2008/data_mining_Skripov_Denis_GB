from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import requests
from lxml import html
from pymongo import MongoClient
from time import sleep


def user_enter():
    user_word = input("Что вводим?")
    enter_phrase = driver.find_element_by_xpath('//input[contains(@placeholder,"Введите фразу или слово")]')
    enter_phrase.clear()
    enter_phrase.send_keys(user_word)
    enter_phrase.send_keys(Keys.ENTER)
    sleep(3)

def scroll(driver):
    for i in range(5):
        post_link = driver.find_elements_by_class_name("post_link")

        actions = ActionChains(driver)
        actions.move_to_element(post_link[-1])
        actions.perform()
        sleep(5)
        if driver.find_elements_by_class_name("JoinForm__notNow"):
            closed = driver.find_element_by_xpath('//a[contains(@class,"JoinForm__notNow")]').click()
            sleep(1)

def link_posts(driver,header):
    all_list = []
    items = driver.find_elements_by_xpath('//a[contains(@class,"post_link")]')
    for item in items:
        link = item.get_attribute('href')


        response = requests.get(link,headers=header)
        dom = html.fromstring(response.text)

        data_posts = {}

        date_post = dom.xpath('//span[@class="rel_date"]/text()')[0].replace("\xa0", " ")

        text_post = dom.xpath('//div[@class="wall_post_text"]/text()')
        text_post = " ".join(text_post)

        q_like =dom.xpath('//div[@class="like_button_count"]/text()')[0]

        try:
            q_reposts = dom.xpath('//div[@class="like_button_count"]/text()')[1]
        except:
            q_reposts = ''

        try:
            q_view = dom.xpath('//div[@class="like_views _views "]/text()')[0]
        except:
            q_view = ''

        data_posts['ссылка'] = link
        data_posts['дата'] = date_post
        data_posts['текст'] = text_post
        data_posts['кол-во лайков'] = q_like
        data_posts['кол-во репостов'] = q_reposts
        data_posts['кол-во просмотров'] = q_view

        all_list.append(data_posts)
    driver.quit()
    return all_list

def save_in_mongo(all_list):
    db_client = MongoClient('localhost', 27017)
    db = db_client['basa_posts']
    posts = db.posts
    posts.insert_many(all_list)

if __name__ == '__main__':

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

    DRAVER_PATH = "./chromedriver/chromedriver.exe"

    url = "https://vk.com/tokyofashion"
    driver = webdriver.Chrome(DRAVER_PATH)
    driver.get(url)
    sleep(2)

    search = driver.find_element_by_xpath('//a[contains(@class,"tab_search")]')
    search.click()
    sleep(2)

    user_enter()
    scroll(driver)
    all_list = link_posts(driver, header)

    save_in_mongo(all_list)













