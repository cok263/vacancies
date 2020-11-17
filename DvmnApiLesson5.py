import requests


base_url = 'https://api.hh.ru/'
url = '{}{}'.format(base_url, 'vacancies')

payload = {
	'area': 2,
	'industry': '7.541',
	'period' : 5,
}

response = requests.get(url, params=payload)
response.raise_for_status()

vacancies = response.json()
programmer_vacancies = []
find_vacancy = 'программист'
#print(response.url)
#print(vacancies)
for vacancy in vacancies['items']:
	if find_vacancy in vacancy['name'].lower():
		programmer_vacancies.append(vacancy)

print(programmer_vacancies)
