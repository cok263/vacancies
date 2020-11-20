import requests
import os
from dotenv import load_dotenv
from collections import defaultdict
from terminaltables import AsciiTable

from sj_tools import popular_languages_info_sj
from hh_tools import popular_languages_info_hh


def get_info_table_instance(title, data):
    vacancies_info = []
    headers = [
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата',
    ]
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
    sj_secret_key = os.getenv('SUPERJOB_SECRET_KEY')

    popular_languages = ('JavaScript', 'Java', 'Python',
                         'Php', 'Ruby', 'C++', 'C', 'Go',)

    print(get_info_table_instance('HeadHunter Moscow',
        popular_languages_info_hh(popular_languages)).table)
    print()
    print(get_info_table_instance('Superjob Moscow',
        popular_languages_info_sj(sj_secret_key, popular_languages)).table)

if __name__ == '__main__':
    main()
