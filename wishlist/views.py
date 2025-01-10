from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import get_user
from logic.services import view_in_wishlist, add_to_wishlist, remove_from_wishlist, add_user_to_wishlist
from store.models import DATABASE


# Create your views here.
@login_required(login_url='login:login_view')
def wishlist_view(request):
    if request.method == "GET":
        current_user = get_user(request).username # TODO прописать отображение избранного. Путь до HTML - wishlist/wishlist.html
        data = view_in_wishlist(request)[current_user]  # TODO Вызвать ответственную за это действие функцию
        if request.GET.get('format') == 'json':
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                             'indent': 4})
        products = []  # Список продуктов
        for id_product in data.get('products'):
            product = DATABASE[id_product]  # 1. Получите информацию о продукте из DATABASE по его product_id. product будет словарём
        #     product['count'] = count  # 2. в словарь product под ключом "quantity" запишите текущее значение товара в корзине
        #     product['price_total'] = round(count * product['price_after'],
        #                                2)  # добавление общей цены позиции с ограничением в 2 знака
        # # 3. добавьте product в список products
            products.append(product)
        return render(request, "wishlist/wishlist.html", context={"products": products})

# @login_required(login_url='login:login_view')
# def wishlist_add_view(request, id_product):
#     if request.method == "GET":
#         result = add_to_wishlist(request, id_product)  # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
#         if result:
#             return JsonResponse({"answer": "Продукт успешно добавлен в избранное"},
#                                 json_dumps_params={'ensure_ascii': False})
#
#         return JsonResponse({"answer": "Неудачное добавление в избранное"},
#                             status=404,
#                             json_dumps_params={'ensure_ascii': False})


@login_required(login_url='login:login_view')
def wishlist_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_wishlist(request, id_product)  # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        if result:
            return redirect("wishlist:wishlist_view")  # TODO Вернуть перенаправление на корзину
        return HttpResponseNotFound("Неудачное удаление из корзины")


# @login_required(login_url='login:login_view')
def wishlist_add_json(request, id_product: str):
    """
    Добавление продукта в избранное и возвращение информации об успехе или неудаче в JSON
    """
    if request.method == "GET":
        result = add_to_wishlist(request,id_product)  # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в избранное"},
                                json_dumps_params={'ensure_ascii': False})
        return JsonResponse({"answer": "Неудачное добавление в избранное"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


# @login_required(login_url='login:login_view')
def wishlist_del_json(request, id_product: str):
    """
    Удаление продукта из избранного и возвращение информации об успехе или неудаче в JSON
    """
    if request.method == "GET":
        result = remove_from_wishlist(request, id_product)  # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        if result:
            return JsonResponse({"answer": "Продукт успешно 7удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})
        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})

@login_required(login_url='login:login_view')
def wishlist_json(request):
    """
    Просмотр всех продуктов в избранном для пользователя и возвращение этого в JSON
    """
    if request.method == "GET":
        current_user = get_user(request).username  # from django.contrib.auth import get_user
        data = view_in_wishlist(request)[current_user]  # TODO Вызвать ответственную за это действие функцию
        if data:
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                 'indent': 4})
        return JsonResponse({"answer": "Пользователь не авторизован"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})