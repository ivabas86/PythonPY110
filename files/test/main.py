import requests

key = 'ddc6cb704e3a4962901192455240412'
lat = '59.894'
lon = '30.264'

url = f'https://api.weatherapi.com/v1/current.json?key={key}&q={lat},{lon}'
response = requests.get(url)
print(response.json())

def current_weather(lat = 59.93, lon = 30.31):
    """
    Описание функции, входных и выходных переменных
    """
    token = '858944cb-71fd-4c75-93ba-8af3b9778936'  # Вставить ваш токен
    url = f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}"  # Если вдруг используете тариф «Погода на вашем сайте»
    # то вместо forecast используйте informers. url = f"https://api.weather.yandex.ru/v2/informers?lat={lat}&lon={lon}"
    headers = {"X-Yandex-API-Key": f"{token}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    return  data

if __name__ == "__main__":
    print(current_weather(59.93, 30.31))