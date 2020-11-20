import requests
from collections import defaultdict

from salary import predict_salary


def predict_rub_salary_sj(vacancy):
    if vacancy['currency'] == 'rub':
        payment_from = int(vacancy['payment_from'])
        payment_to = int(vacancy['payment_to'])
        return predict_salary(payment_from, payment_to)


def popular_languages_info_sj(secret, popular_languages):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': secret,
    }

    find_params = {
        't': 4,
        'catalogues': 'Разработка, программирование',
    }

    languages_info = {}

    for language in popular_languages:
        language_info = defaultdict(int)
        find_params['keywords'] = ['Программист', language]
        count_proceeded = 0
        sum_proceeded = 0
        page = 0
        page_data = {'more': True}

        while page_data['more']:
            find_params['page'] = page
            page += 1
            page_response = requests.get(url, params=find_params,
                                         headers=headers)
            page_response.raise_for_status()
            page_data = page_response.json()

            for vacancy in page_data['objects']:
                predict_salary = predict_rub_salary_sj(vacancy)
                if predict_salary:
                    sum_proceeded += int(predict_salary)
                    count_proceeded += 1

            if not page_data['more']:
                break

        language_info['vacancies_found'] = page_data['total']
        language_info['vacancies_processed'] = count_proceeded
        language_info['average_salary'] = int(sum_proceeded/count_proceeded)
        languages_info[language] = language_info

    return languages_info
