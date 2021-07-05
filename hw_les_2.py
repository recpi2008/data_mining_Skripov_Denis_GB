import json
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
from time import sleep


class HHscraper:
    def __init__(self, start_url, headers, params):
        self.start_url = start_url
        self.start_headers = headers
        self.start_params = params
        self.info_vacance = []


    def get_html_string(self, url, headers='', params=''):
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.ok:
                return response.text

        except Exception as e:
            sleep(1)
            print(e)
            return None

    @staticmethod
    def get_dom(html_string):
        return bs(html_string, "html.parser")

    def run(self):
        next_butten_hh = ''
        while  next_butten_hh != None:
            if next_butten_hh == '':
                html_string = self.get_html_string(self.start_url + '/search/vacancy', self.start_headers,
                                                   self.start_params)
            else:
                html_string = self.get_html_string(next_butten_hh)

            soup = HHscraper.get_dom(html_string)
            vacance_list = soup.findAll('div', attrs={'class': 'vacancy-serp-item'})
            self.get_info_from_element(vacance_list)
            try:
                next_butten_hh = self.start_url + soup.find('a', attrs={'data-qa': 'pager-next'}).attrs["href"]
            except Exception as e:
                next_butten_hh = None

    def get_info_from_element(self, vacance_list):

        for vacance in vacance_list:
            vacance_data = {}
            vacance_name = vacance.find('a', {'class': 'bloko-link'}).getText()
            vacance_link = vacance.find('a', {'class': 'bloko-link'}).attrs["href"]
            vacance_data['имя вакансии'] = vacance_name
            vacance_data['ссылка на вакансию'] = vacance_link
            vacance_data['источник'] = self.start_url
            self.get_salary(vacance_data, vacance)
            self.info_vacance.append(vacance_data)

    def get_salary(self, vacance_data, vacance):
        try:
            vacance_salary = vacance.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText()
            vacance_salary = vacance_salary.replace('\u202f', '').split()
            if '–' in vacance_salary:
                vacance_data['мин зарплата'] = float(vacance_salary[0])
                vacance_data['макс зарплата'] = float(vacance_salary[2])
                vacance_data['валюта'] = vacance_salary[-1]
            elif 'от' in vacance_salary:
                vacance_data['мин зарплата'] = float(vacance_salary[1])
                vacance_data['валюта'] = vacance_salary[-1]
            elif 'до' in vacance_salary:
                vacance_data['макс зарплата'] = float(vacance_salary[1])
                vacance_data['валюта'] = vacance_salary[-1]

        except Exception as e:
            vacance_data['зарплата'] = None

    def save_info_vacance(self):
        with open("vacancy_hh.json", 'w', encoding="utf-8") as file:
            json.dump(self.info_vacance, file, indent=2, ensure_ascii=False)


class SJscraper:
    def __init__(self, start_url, headers, params):
        self.start_url = start_url
        self.start_headers = headers
        self.start_params = params
        self.info_sj_vacance = []

    def get_html_string(self, url, headers='', params=''):
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.ok:
                return response.text

        except Exception as e:
            sleep(1)
            print(e)
            return None

    @staticmethod
    def get_dom(html_string):
        return bs(html_string, "html.parser")

    def run(self):
        next_butten_sj = ''
        while next_butten_sj != None:
            if next_butten_sj == '':
                html_string = self.get_html_string(self.start_url + "vacancy/search/", self.start_headers,
                                                   self.start_params)
            else:
                html_string = self.get_html_string(next_butten_sj)

            soup = SJscraper.get_dom(html_string)
            vacance_list = soup.findAll('div',{'class':'iJCa5 f-test-vacancy-item _1fma_ _2nteL'})
            self.get_info_from_element(vacance_list)
            try:
                next_butten_sj = main_link_sj + soup.find('a', attrs={'class': 'f-test-button-dalshe'}).attrs["href"]

            except Exception as e:
                next_butten_sj = None

    def get_info_from_element(self, vacance_list):
        for vacancy in vacance_list:
            vacancy_sj_data = {}
            vacancy_sj_name = vacancy.find("a", {'class': 'icMQ_'}).getText()
            vacancy_sj_link = main_link_sj + vacancy.find('a', {'class': 'icMQ_'}).attrs["href"]
            vacancy_sj_data['имя вакансии'] = vacancy_sj_name
            vacancy_sj_data['ссылка на вакансию'] = vacancy_sj_link
            vacancy_sj_data['источник'] = self.start_url
            self.get_salary(vacancy_sj_data, vacancy)
            self.info_sj_vacance.append(vacancy_sj_data)

    def get_salary(self, vacancy_sj_data, vacancy):
        try:
            vacancy_sj_salary = vacancy.find("span",
                                             {'class': "_1OuF_ _1qw9T f-test-text-company-item-salary"}).getText()
            if '—' in vacancy_sj_salary:
                sal = vacancy_sj_salary.replace('\xa0', ' ').split()
                if sal[0].isdigit() and sal[1].isdigit():
                    mim_sal = sal[0] + sal[1]
                    vacancy_sj_data['мин зарплата'] = float(mim_sal)
                else:
                    vacancy_sj_data['мин зарплата'] = float(sal[0])
                if sal[-3].isdigit() and sal[-2].isdigit():
                    max_sal = sal[-3] + sal[-2]
                    vacancy_sj_data['макс зарплата'] = float(max_sal)
                else:
                    vacancy_sj_data['макс зарплата'] = float(sal[-3])
                vacancy_sj_data['валюта'] = sal[-1]
            elif 'По' in vacancy_sj_salary:
                vacancy_sj_data['зарплата'] = "По договоренности"
                vacancy_sj_data['валюта'] = None
            elif 'от' in vacancy_sj_salary:
                sal = vacancy_sj_salary.replace('\xa0', ' ').split()
                if sal[1].isdigit() and sal[2].isdigit():
                    mim_sal = sal[1] + sal[2]
                    vacancy_sj_data['мин зарплата'] = float(mim_sal)
                else:
                    vacancy_sj_data['мин зарплата'] = float(sal[1])
                vacancy_sj_data['валюта'] = sal[-1]
            elif 'до' in vacancy_sj_salary:
                sal = vacancy_sj_salary.replace('\xa0', ' ').split()
                if sal[1].isdigit() and sal[2].isdigit():
                    max_sal = sal[1] + sal[2]
                    vacancy_sj_data['макс зарплата'] = float(max_sal)
                else:
                    vacancy_sj_data['макс зарплата'] = float(sal[1])
                vacancy_sj_data['валюта'] = sal[-1]
            else:
                sal = vacancy_sj_salary.replace('\xa0', ' ').split()
                if sal[0].isdigit() and sal[1].isdigit():
                    user_sal = sal[0] + sal[1]
                    vacancy_sj_data['макс зарплата'] = float(user_sal)
        except:
            vacancy_sj_data['зарплата'] = None

    def save_info_vacance(self):
        with open("vacancy_sj.json", 'w', encoding="utf-8") as file:
            json.dump(self.info_sj_vacance, file, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    user_find = input('Введите вакансию:\n')

    main_link_hh = "https://hh.ru"
    params_main_hh = {"area": "1",
                   "fromSearchLine": "true",
                   "st": "searchVacancy",
                   "text": user_find,
                   "page": "0"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}

    scraper_hh = HHscraper(main_link_hh, headers, params_main_hh)
    scraper_hh.run()
    scraper_hh.save_info_vacance()

    main_link_sj = "https://www.superjob.ru/"
    params_sj = {"keywords": user_find,
                 "geo%5Bt%5D%5B0%5D": "4"}
    scraper_sj = SJscraper(main_link_sj, headers, params_sj)
    scraper_sj.run()
    scraper_sj.save_info_vacance()