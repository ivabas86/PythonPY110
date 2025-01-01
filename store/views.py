import requests
import codecs
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import render
from logic.services import view_in_cart, remove_from_cart, add_to_cart
from store.models import DATABASE
from logic.services import filtering_category

# Create your views here.
def product_(request):
    if request.method == 'GET':
        id_ = request.GET.get("id")
        if id_:
            if id_ in DATABASE:
                return JsonResponse(DATABASE.get(id_),json_dumps_params={'ensure_ascii': False, 'indent': 4})
            return HttpResponseNotFound('Данного продукта нет в базе данных')
        category_key = request.GET.get("category")
        ordering_key = request.GET.get('ordering')
        reverse_key = request.GET.get('reverse')
        if ordering_key:
            if str(reverse_key).lower() == 'true':
                data = filtering_category(DATABASE, category_key, ordering_key,  True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})

def shop_view(request):
    if request.method == 'GET':
        # with open('store/shop.html', encoding= 'utf-8') as f:
        #     data = f.read()
        # return HttpResponse(data)
        return render(request, 'store/shop.html', context= {'products': DATABASE.values()})

def product_page_view(request, page):
    if request.method == 'GET':
        if isinstance (page, str):
            for prod in DATABASE.values():
                if prod ['html'] == page:
                    with open (f'store/products/{page}.html', encoding= 'utf-8') as f:
                        data = f.read()
                    return HttpResponse(data)
        elif isinstance(page, int):
            prod = DATABASE.get(str(page))
            if prod:
                with open(f'store/products/{prod["html"]}.html', encoding= 'utf-8') as f:
                    data = f.read()
                return HttpResponse(data)

def cart_view(request):
    if request.method == "GET":
        data = view_in_cart()  # TODO Вызвать ответственную за это действие функцию
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})

def cart_add_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(id_product)  # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})

def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(id_product)  # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})