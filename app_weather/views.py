import json
from datetime import datetime
import requests
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from weather_api import current_weather

# Create your views here.
from django.http import JsonResponse

def my_view(request):
    if request.method == "GET":
        data = current_weather(city='Luga')  # Результат работы функции current_weather
        # А возвращаем объект JSON. Параметр json_dumps_params используется, чтобы передать ensure_ascii=False
        # как помните это необходимо для корректного отображения кириллицы
        return JsonResponse(data, safe = False, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})
def weather_view(request):
    if request.method == "GET":
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        if lat and lon:
            data = current_weather(lat=lat, lon = lon)
        else:
            data = current_weather(59.93, 30.31)
        return JsonResponse(data, safe = False, json_dumps_params={'ensure_ascii': False, 'indent': 4})


# def current_weather(lat, lon1):
#     """
#     Описание функции, входных и выходных переменных
#     """
#     token = '858944cb-71fd-4c75-93ba-8af3b9778936'  # Вставить ваш токен
#     url = f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon1}"  # Если вдруг используете тариф «Погода на вашем сайте»
#     # то вместо forecast используйте informers. url = f"https://api.weather.yandex.ru/v2/informers?lat={lat}&lon={lon}"
#     headers = {"X-Yandex-API-Key": f"{token}"}
#     response = requests.get(url, headers=headers)
#     data = response.json()
#
#     # Данная реализация приведена для тарифа «Тестовый», если у вас Тариф «Погода на вашем сайте», то закомментируйте пару строк указанных ниже
#     result = {
#         # 'city': data['location']['region','name','country'],  # Если используете Тариф «Погода на вашем сайте», то закомментируйте эту строку
#         'time': datetime.fromtimestamp(data['fact']['uptime']).strftime("%H:%M"),  # Если используете Тариф «Погода на вашем сайте», то закомментируйте эту строку
#         'temp': data['fact']['temp'],  # TODO Реализовать вычисление температуры из данных полученных от API
#         'feels_like_temp': data['fact']['feels_like'],  # TODO Реализовать вычисление ощущаемой температуры из данных полученных от API
#         'pressure': data['fact']['feels_like'],  # TODO Реализовать вычисление давления из данных полученных от API
#         'humidity': data['fact']['humidity'],  # TODO Реализовать вычисление влажности из данных полученных от API
#         'wind_speed': data['fact']['wind_speed'],  # TODO Реализовать вычисление скорости ветра из данных полученных от API
#         'wind_gust': data['fact']['wind_gust'],  # TODO Реализовать вычисление скорости порывов ветка из данных полученных от API
#         # 'wind_dir': DIRECTION_TRANSFORM.get(data['fact']['wind_dir']),  # Если используете Тариф «Погода на вашем сайте», то закомментируйте эту строку
#     }
#     return result
#
#
# if __name__ == "__main__":
#     print(current_weather(59.93, 30.31))  # Проверка работы для координат Санкт-Петербурга



