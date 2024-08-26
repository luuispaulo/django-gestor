from django.urls import path, include, reverse_lazy
from shopee.views import views_auth 

app_name = 'shopee'

urlpatterns = [
    path('shopee/auth/authorize/',views_auth.authorize ,name='authorize_shopee'),
    path('shopee/auth/callback/',views_auth.callback ,name='callback_shopee'),
    path('shopee/auth/new_refresh_token/',views_auth.refresh_token ,name='refresh_token_shopee'),
]