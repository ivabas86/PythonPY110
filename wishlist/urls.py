from django.urls import path

from store.views import product_page_view
from wishlist.views import wishlist_view, wishlist_del_view, wishlist_del_json, wishlist_add_json, \
    wishlist_json

#  TODO Импортируйте ваше представление

app_name = 'wishlist'

urlpatterns = [
    path('wishlist/', wishlist_view, name='wishlist_view'),  # TODO Зарегистрируйте обработчик
    # path('wishlist/add/<str:id_product>', wishlist_add_view),
    path('wishlist/del/<str:id_product>', wishlist_del_view, name = 'del_now'),
    path('product/<slug:page>.html', product_page_view, name = "product_page_view"),
    path('product/<int:page>', product_page_view),
    path('wishlist/api/add/<str:id_product>', wishlist_add_json),
    path('wishlist/api/del/<str:id_product>', wishlist_del_json),
    path('wishlist/api/', wishlist_json),
]