import json
from http.client import HTTPResponse

import requests
from datetime import datetime

from django.http import JsonResponse, HttpResponse

# Словарь перевода значений направления ветра
DIRECTION_TRANSFORM = {
    'n': 'северное',
    'nne': 'северо - северо - восточное',
    'ne': 'северо - восточное',
    'ene': 'восточно - северо - восточное',
    'e': 'восточное',
    'ese': 'восточно - юго - восточное',
    'se': 'юго - восточное',
    'sse': 'юго - юго - восточное',
    's': 'южное',
    'ssw': 'юго - юго - западное',
    'sw': 'юго - западное',
    'wsw': 'западно - юго - западное',
    'w': 'западное',
    'wnw': 'западно - северо - западное',
    'nw': 'северо - западное',
    'nnw': 'северо - северо - западное',
    'c': 'штиль',
}


def current_weather(lat=None,lon=None,city=None):
    token = "a98a1ca923944aecb4f211406242212"
    if lat and lon:
        url = f'https://api.weatherapi.com/v1/current.json?key={token}&q= {lat},{lon}'
        response = requests.get(url)

    else:
        params = {'key': token, 'q': city}
        url = f'https://api.weatherapi.com/v1/current.json'
        response = requests.get(url, params=params)
    # print(response.text)
    data = response.json()
    time_ = datetime.fromisoformat(data["current"]["last_updated"]).time()
    date_ = '.'.join(list(reversed(str(datetime.fromisoformat(data["current"]["last_updated"]).date()).split('-'))))
    # print(json.dumps(data, indent=4))
    # s = [f'Город: {data["location"]["name"]}',
    #     f'Страна: {data["location"]["country"]}',
    #     f'Температура: {data["current"]["temp_c"]} град',
    #     f'Ветер: {data["current"]["wind_kph"]} км/ч\n',
    #     f'Ощущается: {data["current"]["feelslike_c"]} град',
    #     f'Время обновления:{time_} {date_}'
    #      ]
    s = {
        'Город': data["location"]["name"],
         'Страна': data["location"]["country"],
         'Температура': f'{data["current"]["temp_c"]} град',
         'Ветер': f'{data["current"]["wind_kph"]}км/ч',
         'Ощущается': f'{data["current"]["feelslike_c"]}град',
         'Время обновления':f'{time_} {date_}'
    }
    return s
