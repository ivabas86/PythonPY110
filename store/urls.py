from django.urls import path
from store.views import product_, shop_view, product_page_view, coupon_chek_view, delivery_estimate_view, \
    cart_buy_now_view, cart_remove_view
from store.views import cart_view,cart_add_view,cart_del_view

app_name = 'store'
urlpatterns = [
    path('product/', product_),
    path('', shop_view, name='shop_view'),
    path('product/<slug:page>.html', product_page_view, name = "product_page_view"),
    path('product/<int:page>', product_page_view),
    path('cart/', cart_view, name = 'cart_view'),
    path('cart/add/<str:id_product>', cart_add_view),
    path('cart/del/<str:id_product>', cart_del_view),
    path('coupon/check/<str:coupon_code>', coupon_chek_view),
    path('delivery/estimate', delivery_estimate_view),
    path('cart/buy/<str:id_product>', cart_buy_now_view, name="buy_now"),
    path('cart/remove/<str:id_product>', cart_remove_view, name="remove_now"),
]