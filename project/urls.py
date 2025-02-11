"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from random import random

from app_datetime.views import datetime_view
from app_weather.views import current_weather
from store.views import product_, shop_view


def random_view(request):
    if request.method == 'GET':
        data = random()
        return HttpResponse(data)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('random/', random_view),
    path('datetime/', datetime_view),
    # path('app_weather/', current_weather),
    path('', include ('store.urls')),
    path('', include ('app_weather.urls')),
    path('', include('app_login.urls')),
    path('', include('wishlist.urls')),
]
