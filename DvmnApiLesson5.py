import requests
import pprint
import time
from collections import defaultdict


def getAreaId(area_name):
    url = 'https://api.hh.ru/suggests/areas'
    payload = {
        'text': area_name,
    }
    areas = requests.get(url, params=payload)
    areas.raise_for_status()
    return int(areas.json()['items'][0]['id'])


def getSpecializationId(specialization_name):
    url = 'https://api.hh.ru/specializations'
    industries = requests.get(url)
    industries.raise_for_status()
    for industry in industries.json():
        if industry['name'] == specialization_name:
            return industry['id']
        else:
            for specialization in industry['specializations']:
                if specialization['name'] == specialization_name:
                    return specialization['id']
    return -1


def predict_rub_salary(vacancy):
    if vacancy['salary'] is not None:
        salary = vacancy['salary']
        if salary['currency'] == 'RUR':
            if salary['from'] is not None:
                if salary['to'] is not None:
                    return (int(salary['from']) + int(salary['to'])) / 2
                else:
                    return int(salary['from']) * 1.2
            else:
                return int(salary['to']) * 0.8
    return None


def popular_languages_info():
    url = 'https://api.hh.ru/vacancies'

    find_params = {
        'area': getAreaId('Москва'),
        'specialization': getSpecializationId('Программирование, Разработка'),
        'period': 30,
        'text': 'программист',
    }

    popular_languages = ('JavaScript', 'Java', 'Python',
                         'Php', 'Ruby', 'C++', 'C', 'Go',)

    languages_info = {}

    max_page=100
    for language in popular_languages:
        
        language_info = defaultdict(int)
        find_params['text'] = 'Программист {}'.format(language)
        
        for page in range(max_page):
            find_params['page'] = page
            page_response = requests.get(url, params=find_params)
            page_response.raise_for_status()
            page_data = page_response.json()

            for vacancy in page_data['items']:
                predict_salary = predict_rub_salary(vacancy)
                if predict_salary is not None:
                    language_info['average_salary'] += int(predict_salary)
                    language_info['vacancies_processed'] += 1


            if page >= page_data['pages']:
                break
        
        language_info['vacancies_found'] = page_data['found']
        language_info['average_salary'] = int(
            language_info['average_salary'] / language_info['vacancies_processed']
        )
        languages_info[language] = language_info

    return languages_info

def print_programmers_info():
    url = 'https://api.hh.ru/vacancies'

    find_params = {
        'area': getAreaId('Москва'),
        'specialization': getSpecializationId('Программирование, Разработка'),
        'period': 30,
        'text': 'программист'
    }

    page_response = requests.get(url, params=find_params)
    page_response.raise_for_status()
    page_data = page_response.json()
    for vacancy in page_data['items']:
        print(vacancy['name'], predict_rub_salary(vacancy))

print_programmers_info()
pprint.pprint(popular_languages_info())