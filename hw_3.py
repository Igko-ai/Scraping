"""Домашнее задание №3
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
записывающую собранные вакансии в созданную БД.
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой
больше введённой суммы.
3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
"""

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint


name_vacancy = 'лесоруб'  # input('Искомая вакансия: ')

url = 'https://hh.ru'
params = {'clusters': 'true',
          'enable_snippets': 'true',
          'salary': None,
          'st': 'searchVacancy',
          'text': name_vacancy
          }
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

response = requests.get(f'{url}/search/vacancy', params=params, headers=headers)

soup = bs(response.text, 'html.parser')

# определяем число страниц
last_page = soup.find_all('a', {'class': 'bloko-button'})[-2].getText()
if last_page.isdigit():
    num_page = int(last_page)
else:
    num_page = 1


# функция обработки предложений по зарплате
def salary(list):
    for el in list:
        data_salary = el.getText().split()
        if data_salary[0] == 'от':
            min_salary = int(data_salary[1] + data_salary[2])
            max_salary = 'None'
            currency = data_salary[-1]
        elif data_salary[0] == 'до':
            min_salary = 'None'
            max_salary = int(data_salary[1] + data_salary[2])
            currency = data_salary[-1]
        elif data_salary[0]:
            min_salary = int(data_salary[0] + data_salary[1])
            max_salary = int(data_salary[3] + data_salary[4])
            currency = data_salary[-1]
        else:
            min_salary = 'None'
            max_salary = 'None'
            currency = 'None'
    return min_salary, max_salary, currency


for i in range(num_page):
    params['page'] = i
    response = requests.get(f'{url}/search/vacancy', params=params, headers=headers)
    soup = bs(response.text, 'html.parser')

    vacancy_list = soup.find_all('span', {'class': 'resume-search-item__name'})
    all_vacancies = []
    vacancies = []
    for vacancy in vacancy_list:
        vacancy_data = {}

        # название вакансии
        vacancy_name = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).getText()

        # ссылка на вакансию
        vacancy_link = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})["href"]

        # минимальная зарплата
        try:
            min_salary = vacancy.find_parent('div').findNextSibling()
            if min_salary:
                vacancy_min_salary = salary(min_salary)[0]
            else:
                None
        except ValueError:
            pass
        else:
            None

        # максимальная зарплата
        try:
            max_salary = vacancy.find_parent('div').findNextSibling()
            if max_salary:
                vacancy_max_salary = salary(max_salary)[1]
            else:
                None
        except ValueError:
            pass
        else:
            None

        # валюта зарплаты
        try:
            currency = vacancy.find_parent('div').findNextSibling()
            if currency:
                vacancy_currency = salary(currency)[2]
        except AttributeError:
            pass
        else:
            None

        # сайт компании-работодателя
        try:
            site = vacancy.find_parent('div').findNextSibling().find_parent('div').findNextSibling().find('a', {
                'data-qa': 'vacancy-serp__vacancy-employer'})['href']
            if site:
                vacancy_site = url + \
                               vacancy.find_parent('div').findNextSibling().find_parent('div').findNextSibling().find(
                                   'a', {'data-qa': 'vacancy-serp__vacancy-employer'})['href']
        except AttributeError:
            pass
        else:
            None

        vacancy_data['name'] = vacancy_name
        vacancy_data['vacancy_link'] = vacancy_link
        vacancy_data['min_salary'] = vacancy_min_salary
        vacancy_data['max_salary'] = vacancy_max_salary
        vacancy_data['currency'] = vacancy_currency
        vacancy_data['company_site'] = vacancy_site
        vacancies.append(vacancy_data)
    all_vacancies.extend(vacancies)

    pprint(list(all_vacancies))

"""
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, 
записывающую собранные вакансии в созданную БД.
2. Написать функцию, которая производит поиск и выводит на экран вакансии 
с заработной платой больше введённой суммы.
3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
"""

from pymongo import MongoClient
import hashlib

client = MongoClient('localhost', 27017)
db = client['hh_base']
hh_vacancies = db.hh_vacancies

# получение хэшей
def hash(i):
    hashId = hashlib.sha1()
    hashId.update(repr(i).encode('utf-8'))
    return hashId.hexdigest()

# запись собранных данных
def to_mongo(data_dict):
    for i in data_dict:
        data_dict['_id'] = hash(i)
        db.hh_vacancies.insert_one(i)

# поиск и вывод вакансий с заработной платой больше введённой суммы
def greater(summa):
    if min_salary:
        print(db.hh_vacancies.find({min_salary: {'$gt': summa}}))
    elif max_salary:
        print(db.hh_vacancies.find({max_salary: {'$gt': summa}}))
    else:
        print('None')

# добавляем новые данные
def new_to_mongo(new_data_dict):
    for j in new_data_dict:
        if new_data_dict[_id] in hh_vacancies:
            pass
        else:
            db.hh_vacancies.insert_one(j)
