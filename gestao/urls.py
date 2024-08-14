#url - view - template
from django.urls import path, include, reverse_lazy
from .views import  Homegestor, Dashboard, Pesquisagestao, Perfil, create_user_view, configuracao_view,IntegracaoListView,IntegracaoCreateView, authorize,callback,get_refresh_token, get_price_info, get_create_product,get_anuncios,MercadoLivreAnuncios
from django.contrib.auth import views as auth_viewgestao
from gestao import views

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
    path('configuracao/', configuracao_view, name='configuracao'),

    path('integracoes/', IntegracaoListView.as_view(), name='integracao_list'),
    path('integracoes/delete/<int:pk>', IntegracaoListView.as_view(), name='integracao_list'),

    path('integracoes/nova/', IntegracaoCreateView.as_view(), name='integracao_create'),
    path('authorize/',authorize,name='authorize'),
    path('callback/',callback, name='callback'),
    path('api/refresh_token/', get_refresh_token.as_view(), name='get_refresh_token'),
    path('get_price_info/', get_price_info.as_view(), name='get_price_info'),
    path('create_product/', get_create_product.as_view(), name='create_product'),

    path('get_anuncios/', get_anuncios.as_view(), name='get_anuncios'),
    path('mercadolivre/anuncios', MercadoLivreAnuncios.as_view(), name='MercadoLivre_anuncios'),

]



##int:pk nomeia as paginas para que não seja necessario repetir a estrutura criando varios paths