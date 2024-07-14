#url - view - template
from django.urls import path, include
from .views import Homepage, Homegestor, Dashboard, Pesquisagestao, Perfil, Criarconta
from django.contrib.auth import views as auth_view

app_name = 'gestao'

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('gestao/', Homegestor.as_view(), name='homegestor'),
    path('gestao/<int:pk>', Dashboard.as_view(), name='dashboard'),
    path('pesquisa/', Pesquisagestao.as_view(), name='pesquisafilme'),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('perfil/', Perfil.as_view(), name='perfil'),
    path('criarconta/', Criarconta.as_view(), name='criarconta')
]


##int:pk nomeia as paginas para que não seja necessario repetir a estrutura criando varios paths