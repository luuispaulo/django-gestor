#url - view - template
from django.urls import path, include
from .views import Homepage, Homegestor, Dashboard, Pesquisagestao

app_name = 'gestao'

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('gestao/', Homegestor.as_view(), name='homegestor'),
    path('gestao/<int:pk>', Dashboard.as_view(),name='dashboard'),
    path('pesquisa', Pesquisagestao.as_view(), name='pesquisafilme')
]

##int:pk nomeia as paginas para que não seja necessario repetir a estrutura criando varios paths