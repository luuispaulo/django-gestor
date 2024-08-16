#url - view - template
from django.urls import path, include, reverse_lazy
from shopee import views 

app_name = 'shopee'

urlpatterns = [
    path('shopee/authorize/',views.authorize_shopee ,name='authorize_shopee'),
    path('shopee/callback/',views.callback_shopee ,name='callback_shopee'),
]



##int:pk nomeia as paginas para que não seja necessario repetir a estrutura criando varios paths