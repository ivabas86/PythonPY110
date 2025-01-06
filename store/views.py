import requests
import codecs
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import render
from unicodedata import category

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
                                                                      "category_product": category_product[:5]})
        return HttpResponse(status=404)
def cart_view(request):
    if request.method == "GET":
        data = view_in_cart()  # TODO Вызвать ответственную за это действие функцию
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