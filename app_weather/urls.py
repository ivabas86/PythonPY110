from app_weather.views import my_view, weather_view
from weather_api import current_weather
from django.urls import path
urlpatterns = [
    path('weather/', my_view),
    path('weather_view/', weather_view)

]