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
    token = "ddc6cb704e3a4962901192455240412"
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
    s = f'Город: {data["location"]["name"]}\n' \
        f'Страна: {data["location"]["country"]}\n' \
        f'Температура: {data["current"]["temp_c"]} град\n' \
        f'Ветер: {data["current"]["wind_kph"]} км/ч\n' \
        f'Ощущается: {data["current"]["feelslike_c"]} град\n' \
        f'Время обновления:{time_} {date_}'

    return (s)
