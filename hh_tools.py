import requests
from collections import defaultdict


def get_area_id_hh(area_name):
    url = 'https://api.hh.ru/suggests/areas'
    payload = {
        'text': area_name,
    }
    areas = requests.get(url, params=payload)
    areas.raise_for_status()
    return int(areas.json()['items'][0]['id'])


def get_specialization_id_hh(specialization_name):
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


def predict_rub_salary_hh(vacancy):
    if vacancy['salary']:
        payment_from = 0
        payment_to = 0
        if vacancy['salary']['from']:
            payment_from = int(vacancy['salary']['from'])
        if vacancy['salary']['to']:
            payment_to = int(vacancy['salary']['to'])
        if vacancy['salary']['currency'] == 'RUR':
            return predict_salary(payment_from, payment_to)


def popular_languages_info_hh(popular_languages):
    url = 'https://api.hh.ru/vacancies'

    find_params = {
        'area': get_area_id_hh('Москва'),
        'specialization': get_specialization_id_hh(
            'Программирование, Разработка'
        ),
        'period': 30,
    }

    languages_info = {}
    for language in popular_languages:
        language_info = defaultdict(int)
        find_params['text'] = 'Программист {}'.format(language)
        count_proceeded = 0
        sum_proceeded = 0
        page = 0

        while True:
            find_params['page'] = page
            page += 1
            page_response = requests.get(url, params=find_params)
            page_response.raise_for_status()
            page_data = page_response.json()

            for vacancy in page_data['items']:
                predict_salary = predict_rub_salary_hh(vacancy)
                if predict_salary:
                    sum_proceeded += int(predict_salary)
                    count_proceeded += 1

            if page >= page_data['pages']:
                break

        language_info['vacancies_found'] = page_data['found']
        language_info['vacancies_processed'] = count_proceeded
        language_info['average_salary'] = int(sum_proceeded/count_proceeded)
        languages_info[language] = language_info

    return languages_info
