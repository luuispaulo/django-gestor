from django.urls import path, include, reverse_lazy
from shopee.views import views_auth
from shopee.views import views_orders

app_name = 'shopee'

urlpatterns = [
    path('shopee/auth/authorize/',views_auth.authorize ,name='authorize_shopee'),
    path('shopee/auth/callback/',views_auth.callback ,name='callback_shopee'),
    path('shopee/auth/new_refresh_token/',views_auth.refresh_token ,name='refresh_token_shopee'),
    path('shopee/product/create/',views_orders.create_product ,name='create_product_shopee'),
]