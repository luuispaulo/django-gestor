#url - view - template
from django.urls import path, include, reverse_lazy
from .views import Homepage, Criarconta
from django.contrib.auth import views as auth_view

app_name = 'gestao_public'

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('criarconta/', Criarconta.as_view(), name='criarconta'),
    path('mudarsenha/', auth_view.PasswordChangeView.as_view(template_name ='perfil.html', success_url=reverse_lazy('gestao:homegestor')), name='mudarsenha')
]


##int:pk nomeia as paginas para que não seja necessario repetir a estrutura criando varios paths