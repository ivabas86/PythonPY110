import requests
import codecs
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, Http404
from django.shortcuts import render
from unicodedata import category
from django.shortcuts import redirect
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
        id_ = request.GET.get("id")
        if id_:
            if id_ in DATABASE:
                return JsonResponse(DATABASE.get(id_), json_dumps_params={'ensure_ascii': False, 'indent': 4})
            return HttpResponseNotFound('Данного продукта нет в базе данных')
        category_key = request.GET.get("category")
        ordering_key = request.GET.get('ordering')
        reverse_key = request.GET.get('reverse')
        if ordering_key:
            if str(reverse_key).lower() == 'true':
                data = filtering_category(DATABASE, category_key, ordering_key, True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)
        return render(request, 'store/shop.html', context= {'products': data, 'category': category_key})

def product_page_view(request, page):
    if request.method == 'GET':
        if isinstance (page, str):
            for prod in DATABASE.values():
                if prod ['html'] == page:
                    category_product = [el for el in filtering_category(DATABASE, category_key= prod['category']) if el['name'] != prod['name']]

                    # with open (f'store/products/{page}.html', encoding= 'utf-8') as f:
                    #     data = f.read()
                    return render(request, "store/product.html", context={"product": prod,
                                                                          "category_product": category_product[:5]})
        elif isinstance(page, int):
            prod = DATABASE.get(str(page))
            if prod:
                category_product = [el for el in filtering_category(DATABASE, category_key=prod['category'])
                                    if el['name'] != prod['name']]
                # with open(f'store/products/{prod["html"]}.html', encoding= 'utf-8') as f:
                #     data = f.read()
                return render(request, "store/product.html", context={"product": prod,
                                                                      "category_product":  category_product[:5]})
        return HttpResponse(status=404)

@login_required(login_url='login:login_view')
def cart_view(request):
    if request.method == "GET":
        current_user = get_user(request).username
        data = view_in_cart(request)[current_user]  # TODO Вызвать ответственную за это действие функцию
        if request.GET.get('format') == 'json':
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})
        products = []  # Список продуктов
        for id_product, count in data.get('products').items():
            product = DATABASE[id_product]  # 1. Получите информацию о продукте из DATABASE по его product_id. product будет словарём
            product['count'] = count # 2. в словарь product под ключом "quantity" запишите текущее значение товара в корзине
            product['price_total'] = round(count * product['price_after'],2)  # добавление общей цены позиции с ограничением в 2 знака
            # 3. добавьте product в список products
            products.append(product)
        return render(request, "store/cart.html", context={"products": products})

@login_required(login_url='login:login_view')
def cart_add_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(request, id_product)  # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})

def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(request, id_product)  # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})

def coupon_chek_view (request, coupon_code):
    DATA_COUPON = {
        "coupon":    {
                       "value": 10,
                       "is_valid": True
                      },
        "coupon_old": {
                       "value": 20,
                        "is_valid": False
                      },
                  }
    if request.method == "GET":
        if coupon_code in DATA_COUPON:
            coupon = DATA_COUPON[coupon_code]
            data = {
                "discount": coupon['value'],
                "is_valid": coupon['is_valid']
                    }
            return JsonResponse(data)
        return HttpResponseNotFound('Неверный купон')

def delivery_estimate_view(request):
    # База данных по стоимости доставки. Ключ - Страна; Значение словарь с городами и ценами; Значение с ключом fix_price
    # применяется если нет города в данной стране
    DATA_PRICE = {
                   "Россия":{
                              "Москва": {"price": 80},
                              "Санкт-Петербург": {"price": 80},
                              "fix_price": 100,
                             },
                  "Беларусь":{
                               "Могилев":{"price": 250},
                               "Витебск":{"price": 140},
                               "fix_price": 300
                             }
                  }
    if request.method == "GET":
        data = request.GET
        country = data.get('country') #получение исходных данных
        city = data.get('city')
        country_in_data = DATA_PRICE.get(country) # проверка наличия полученных исходных данных в базе цен
        city_in_data = country_in_data.get(city)
        # TODO Реализуйте логику расчёта стоимости доставки, которая выполняет следующее:
        # Если в базе DATA_PRICE есть и страна (country) и существует город(city), то вернуть JsonResponse со словарём, {"price": значение стоимости доставки}
        # Если в базе DATA_PRICE есть страна, но нет города, то вернуть JsonResponse со словарём, {"price": значение фиксированной стоимости доставки}
        # Если нет страны, то вернуть HttpResponseNotFound("Неверные данные")
        if country_in_data:
            if city_in_data:
                return JsonResponse({"price": city_in_data['price']})
            return JsonResponse({"price": country_in_data['fix_price']})
        return HttpResponseNotFound ('Неверные данные')

@login_required(login_url='login:login_view')
def cart_buy_now_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(request, id_product)
        if result:
            return redirect("store:cart_view")
        return HttpResponseNotFound("Неудачное добавление в корзину")

def cart_remove_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(request, id_product)  # TODO Вызвать функцию удаления из корзины
        if result:
            return redirect("store:cart_view")  # TODO Вернуть перенаправление на корзину

        return HttpResponseNotFound("Неудачное удаление из корзины")


  #
# def cart_view(request):
#     if request.method == "GET":
#         data = view_in_cart()  # TODO Вызвать ответственную за это действие функцию
#         if request.GET.get('format') == 'json':
#             return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
#                                                          'indent': 4})
#         products = []  # Список продуктов
#         for id_product, count in data.get('products').items():
#             product = DATABASE[
#                 id_product]  # 1. Получите информацию о продукте из DATABASE по его product_id. product будет словарём
#             product[
#                 'count'] = count  # 2. в словарь product под ключом "quantity" запишите текущее значение товара в корзине
#             product['price_total'] = round(count * product['price_after'],
#                                            2)  # добавление общей цены позиции с ограничением в 2 знака
#             # 3. добавьте product в список products
#             products.append(product)
#         return render(request, "store/cart.html", context={"products": products})
#
#
# def cart_add_view(request, id_product):
#     if request.method == "GET":
#         result = add_to_cart(id_product)  # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
#         if result:
#             return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
#                                 json_dumps_params={'ensure_ascii': False})
#
#         return JsonResponse({"answer": "Неудачное добавление в корзину"},
#                             status=404,
#                             json_dumps_params={'ensure_ascii': False})
#
#
# def cart_del_view(request, id_product):
#     if request.method == "GET":
#         result = remove_from_cart(
#             id_product)  # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
#         if result:
#             return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
#                                 json_dumps_params={'ensure_ascii': False})
#
#         return JsonResponse({"answer": "Неудачное удаление из корзины"},
#                             status=404,
#                             json_dumps_params={'ensure_ascii': False})