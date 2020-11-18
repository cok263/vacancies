import requests
import os
import pprint
from dotenv import load_dotenv
from collections import defaultdict
from terminaltables import AsciiTable

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


def predict_salary(salary_from, salary_to):
    if salary_from > 0:
        if salary_to > 0:
            return (int(salary_from) + int(salary_to)) / 2
        else:
            return int(salary_from) * 1.2
    elif salary_to > 0:
        return int(salary_to) * 0.8
    return None


def predict_rub_salary_hh(vacancy):
    if vacancy['salary'] is not None:
        payment_from = 0
        payment_to = 0
        if vacancy['salary']['from'] is not None:
            payment_from = int(vacancy['salary']['from'])
        if vacancy['salary']['to'] is not None:
            payment_to = int(vacancy['salary']['to'])
        if vacancy['salary']['currency'] == 'RUR':
            return predict_salary(payment_from, payment_to)
    return None

    
def predict_rub_salary_sj(vacancy):
    if vacancy['currency'] == 'rub':
        payment_from = int(vacancy['payment_from'])
        payment_to = int(vacancy['payment_to'])
        return predict_salary(payment_from, payment_to)
    return None


def popular_languages_info_hh():
    url = 'https://api.hh.ru/vacancies'

    find_params = {
        'area': getAreaId('Москва'),
        'specialization': getSpecializationId('Программирование, Разработка'),
        'period': 30,
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
                predict_salary = predict_rub_salary_hh(vacancy)
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


def popular_languages_info_sj():
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': secret,
    }

    find_params = {
        't': 4,
    }
    popular_languages = ('JavaScript', 'Java', 'Python',
                         'Php', 'Ruby', 'C++', 'C', 'Go',)

    languages_info = {}

    max_page=500
    for language in popular_languages:
        
        language_info = defaultdict(int)
        find_params['keywords'] = ['Программист', language]
        
        for page in range(max_page):
            find_params['page'] = page
            page_response = requests.get(url, params=find_params, headers=headers)
            page_response.raise_for_status()
            page_data = page_response.json()

            for vacancy in page_data['objects']:
                predict_salary = predict_rub_salary_sj(vacancy)
                if predict_salary is not None:
                    language_info['average_salary'] += int(predict_salary)
                    language_info['vacancies_processed'] += 1

            if not page_data['more']:
                break
        
        language_info['vacancies_found'] = page_data['total']
        language_info['average_salary'] = int(
            language_info['average_salary'] / language_info['vacancies_processed']
        )
        languages_info[language] = language_info

    return languages_info


def print_programmers_info_hh():
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
        print(vacancy['name'], predict_rub_salary_hh(vacancy))


def print_programmers_info_sj():
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': secret,
    }

    find_params = {
        't': 4,
        'keywords': ['программист', 'java']
    }

    response = requests.get(url, params=find_params, headers=headers)
    response.raise_for_status()

    #print(response.json())
    vacancies = response.json()['objects']

    for vacancy in vacancies:
        print(vacancy['profession'], vacancy['town']['title'], predict_rub_salary_sj(vacancy), sep=', ')


def get_info_table_instance(title, data):
    vacancies_info = []
    headers = ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    vacancies_info.append(headers)
    for language, info in data.items():
        vacancies_info.append([
            language,
            info['vacancies_found'],
            info['vacancies_processed'],
            info['average_salary']
        ])

    table_instance = AsciiTable(vacancies_info, title)
    return table_instance


def main():
    load_dotenv()
    secret = os.getenv('SUPERJOB_SECRET')

    print(get_info_table_instance('Superjob Moscow', popular_languages_info_hh()).table)
    print()
    print(get_info_table_instance('HeadHunter Moscow', popular_languages_info_sj()).table)

if __name__ == '__main__':
    main()