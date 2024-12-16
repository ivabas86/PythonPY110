import requests
import codecs
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
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
        with open('store/shop.html', encoding= 'utf-8') as f:
            data = f.read()
        return HttpResponse(data)

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


