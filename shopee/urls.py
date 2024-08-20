from django.urls import path, include, reverse_lazy
from shopee import views 

app_name = 'shopee'

urlpatterns = [
    path('shopee/auth/authorize/',views.authorize ,name='authorize_shopee'),
    path('shopee/auth/callback/',views.callback ,name='callback_shopee'),
    path('shopee/auth/new_refresh_token/',views.refresh_token ,name='refresh_token_shopee'),
]