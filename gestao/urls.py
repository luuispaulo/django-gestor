#url - view - template
from django.urls import path, include, reverse_lazy
from .views import  Homegestor, Dashboard, Pesquisagestao, Perfil, create_user_view
from django.contrib.auth import views as auth_viewgestao

app_name = 'gestao'

urlpatterns = [
    path('gestao/', Homegestor.as_view(), name='homegestor'),
    path('gestao/<int:pk>', Dashboard.as_view(), name='dashboard'),
    path('pesquisa/', Pesquisagestao.as_view(), name='pesquisafilme'),
    path('perfil/<int:pk>', Perfil.as_view(), name='perfil'),
    path('mudarsenha/', auth_viewgestao.PasswordChangeView.as_view(template_name ='perfil.html', success_url=reverse_lazy('gestao:homegestor')), name='mudarsenha'),
    path('gestao_public/', include('gestao_public.urls')),
    path('logout/', auth_viewgestao.LogoutView.as_view(template_name ='logout.html'), name='logout'),
    path('create_user/', create_user_view, name='create_user'),
    path('login/', auth_viewgestao.LoginView.as_view(template_name='login.html'), name='login'),
]


##int:pk nomeia as paginas para que não seja necessario repetir a estrutura criando varios paths