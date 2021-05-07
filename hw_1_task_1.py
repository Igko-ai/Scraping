"""1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
для конкретного пользователя, сохранить JSON-вывод в файле *.json"""

import requests
from pprint import pprint
import json

username = 'Igko-ai'
token = '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'

response = requests.get('https://api.github.com/user', auth=(username, token))

# print(response.status_code)
# j_data = response.json()
# pprint(j_data)

repo = requests.get(f'https://api.github.com/users/{username}/repos')

# print(repo.status_code)
# jr_data = repo.json()
# pprint(jr_data)

for i in repo.json():
    print(i['name'])

with open('repo.json', 'w') as f:
    for i in repo.json():
        json.dump(i['name'], f)

with open('data.json', 'w') as f:
    json.dump(response.json(), f)