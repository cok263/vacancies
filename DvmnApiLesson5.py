import requests
import pprint
from collections import defaultdict


def getAreaId(area_name):
    url = '{}{}'.format(base_url, '/suggests/areas')
    payload = {
        'text': area_name,
    }
    areas = requests.get(url, params=payload)
    areas.raise_for_status()
    return int(areas.json()['items'][0]['id'])


def getSpecializationId(specialization_name):
    url = '{}{}'.format(base_url, '/specializations')
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

    find_params = {
        'area': getAreaId('Москва'),
        'specialization': getSpecializationId('Программирование, Разработка'),
        'period': 30,
        'text': 'программист',
    }

    popular_languages = ('JavaScript', 'Java', 'Python',
                         'Php', 'Ruby', 'C++', 'C', 'Go',)

    languages_info = {}

    for language in popular_languages:
        language_info = defaultdict(int)

        find_params['text'] = 'Программист {}'.format(language)
        page_response = requests.get(url, params=find_params)
        page_response.raise_for_status()
        page_data = page_response.json()

        for vacancy in page_data['items']:
            predict_salary = predict_rub_salary(vacancy)
            if predict_salary is not None:
                language_info['average_salary'] += int(predict_salary)
                language_info['vacancies_processed'] += 1

        language_info['vacancies_found'] = page_data['found']
        language_info['average_salary'] = int(
            language_info['average_salary'] / language_info['vacancies_processed']
        )
        languages_info[language] = language_info
    return languages_info




base_url = 'https://api.hh.ru'
url = '{}{}'.format(base_url, '/vacancies')

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
    #print(vacancy['name'], vacancy['salary'])
    print(vacancy['name'], predict_rub_salary(vacancy))

pprint.pprint(popular_languages_info())




'''
vacancies_pages = []
max_page=100


for page in range(max_page):
    find_params['page'] = page
    page_response = requests.get(url, params=find_params)
    page_response.raise_for_status()

    page_data = page_response.json()
    if page >= page_data['pages']:
        break

    vacancies_pages.append(page_data)

programmer_vacancies = []
find_vacancy = 'программист'
for vacancies_page in vacancies_pages:
    for vacancy in vacancies_page['items']:
        if find_vacancy in vacancy['name'].lower():
            programmer_vacancies.append(vacancy)

print(len(programmer_vacancies))
for vac in programmer_vacancies:
    for lang in popular_languages:
        if lang.lower() in vac['name'].lower():
            popular_languages[lang] += 1

pprint.pprint(popular_languages)
'''