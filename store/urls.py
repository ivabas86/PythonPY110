from django.urls import path
from store.views import product_, shop_view, product_page_view
from store.views import cart_view,cart_add_view,cart_del_view

app_name = 'store'
urlpatterns = [
    path('product/', product_),
    path('', shop_view),
    path('product/<slug:page>.html', product_page_view, name = "product_page_view"),
    path('product/<int:page>', product_page_view),
    path('cart/', cart_view),
    path('cart/add/<str:id_product>', cart_add_view),
    path('cart/del/<str:id_product>', cart_del_view),
]