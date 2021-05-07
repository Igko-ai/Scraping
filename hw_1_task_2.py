"""Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
Найти среди них любое, требующее авторизацию (любого типа).
Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл."""

import requests
from pprint import pprint
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
url1 = 'https://api.vk.com/method/users.get'
params1 = {'user_ids' : '6654321',
          'fields' : 'bdate',
          'access_token': '51e4370ebfdecb2430d281deff11bc89cca8c67b3774b288bdb53c8fbb27f33590e14f696c475fb22fb04',
          'v': '5.52'}

# общая информация
response = requests.get(url1, params=params1, headers=headers)

print(response.status_code)

if response.ok:
    print(response.text)

j_data = response.json()
pprint(j_data)

with open('info.json', 'w') as f:
    json.dump(response.json(), f)

# друзья он-лайн
url2 = 'https://api.vk.com/method/friends.getOnline'
params2 = {'user_id' : '6654321',
           'online_mobile' : "1",
          'access_token': '51e4370ebfdecb2430d281deff11bc89cca8c67b3774b288bdb53c8fbb27f33590e14f696c475fb22fb04',
          'v': '5.52'}

friends = requests.get(url2, params=params2, headers=headers)

print(friends.status_code)

if friends.ok:
    print(friends.text)

jf_data = friends.json()
pprint(jf_data)

with open('friends.json', 'w') as f:
    json.dump(friends.json(), f)