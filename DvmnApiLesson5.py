import requests
import pprint


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


base_url = 'https://api.hh.ru'
url = '{}{}'.format(base_url, '/vacancies')

find_params = {
    'area': getAreaId('Москва'),
    'specialization': getSpecializationId('Программирование, Разработка'),
    'period': 30,
    'text': 'программист'

}

popular_languages = {
    'JavaScript': 0,
    'Java': 0,
    'Python': 0,
    'Php': 0,
    'Ruby': 0,
    'C++': 0,
    'C': 0,
    'Go': 0,
}

page_response = requests.get(url, params=find_params)
page_response.raise_for_status()
page_data = page_response.json()
for vacancy in page_data['items']:
    print(vacancy['name'], vacancy['salary'])


for language in popular_languages:
    find_params['text'] = 'Программист {}'.format(language)
    page_response = requests.get(url, params=find_params)
    page_response.raise_for_status()
    page_data = page_response.json()
    popular_languages[language] = page_data['found']

pprint.pprint(popular_languages)



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