from django.urls import path
from store.views import product_, shop_view, product_page_view

urlpatterns = [
    path('product/', product_),
    path('', shop_view),
    path('product/<slug:page>.html', product_page_view),
    path('product/<int:page>', product_page_view)
]