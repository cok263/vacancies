import requests
import os
from dotenv import load_dotenv


load_dotenv()
secret = os.getenv('SUPERJOB_SECRET')

url = 'https://api.superjob.ru/2.0/vacancies/'
headers = {
	'X-Api-App-Id': secret,
}

find_params = {
	#'period': 7,
	't': 4,
}

response = requests.get(url, params=find_params, headers=headers)
response.raise_for_status()

vacancies = response.json()['objects']

for vacancy in vacancies:
	print(vacancy['profession'], vacancy['town']['title'], sep=', ')