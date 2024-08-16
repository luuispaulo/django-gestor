from django.shortcuts import render, redirect, reverse, get_object_or_404
from typing import Any
from django.db.models.query import QuerySet
from .models import relatorio, meli_237330330, configuracao,MercadoLivreAuth,integracao, Orders, MercadoLivreAnuncios
from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView,CreateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tenants.utils import schema_context
from gestao_public.models import Tenant
from .forms import CreateUserForm, FormHomePage, ConfiguracaoForm, MeliFilterForm, FormIntegracao
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
import requests
import json
import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from decimal import Decimal

class Homegestor(LoginRequiredMixin, ListView):
    template_name = 'homegestor.html'
    model = Orders
    context_object_name = 'orders_list'
    paginate_by = 20  # Adicione paginação se necessário

    def get_queryset(self):

        queryset = super().get_queryset()
        self.filter_form = MeliFilterForm(self.request.GET)
        if self.filter_form.is_valid():
            if self.filter_form.cleaned_data['id_venda']:
                queryset = queryset.filter(id_venda__icontains=self.filter_form.cleaned_data['id_venda'])
            if self.filter_form.cleaned_data['titulo_anuncio']:
                queryset = queryset.filter(titulo_anuncio__icontains=self.filter_form.cleaned_data['titulo_anuncio'])
            # Adicione outros filtros conforme necessário

        # Adicionar ordenação
        order_by = self.request.GET.get('order_by')
        if order_by:
            queryset = queryset.order_by(order_by)

        configuracao_obj = configuracao.objects.first()
        
        imposto = Decimal(configuracao_obj.imposto)
        embalagem = Decimal(configuracao_obj.embalagem)
        publicidade = Decimal(configuracao_obj.publicidade)
        transporte = Decimal(configuracao_obj.transporte)
        custofixo = Decimal(configuracao_obj.custofixo)
        CMV = Decimal(configuracao_obj.CMV)

        # Adicionando lucratividade a cada objeto no queryset
        for meli in queryset:
            meli.valor_imposto = meli.valor_pedido * (imposto / Decimal(100))
            meli.valor_cmv = meli.valor_pedido * (CMV / Decimal(100))
            meli.valor_embalagem = meli.valor_pedido * (embalagem / Decimal(100))
            meli.valor_publicidade = meli.valor_pedido * (publicidade / Decimal(100))
            meli.valor_transporte = meli.valor_pedido * (transporte / Decimal(100))
            meli.margem = meli.repasse - meli.valor_imposto - meli.valor_cmv - meli.valor_embalagem - meli.valor_publicidade - meli.valor_transporte
            meli.porcentagem = round ((meli.margem / meli.valor_pedido) * 100,2)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['configuracao_list'] = configuracao.objects.all()
        return context

class Dashboard(LoginRequiredMixin, DetailView):
    template_name = 'dashboard.html'
    model = relatorio

    #object_list

class Pesquisagestao(LoginRequiredMixin, ListView):
    template_name = 'pesquisa.html'
    model = relatorio
        
        ##pesquisa conforme object lista ou none se
    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = relatorio.objects.filter(nome__icontains=termo_pesquisa)
            return object_list
        else:
            return None
        
class Perfil(LoginRequiredMixin, UpdateView):
    template_name = 'perfil.html'
    model = User
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('gestao:homegestor')

def create_user_view(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            tenant_name = form.cleaned_data['tenant_name']
            
            try:
                # Obter o tenant específico
                tenant = Tenant.objects.get(name=tenant_name)
                
                # Usar o contexto do schema do tenant
                with schema_context(tenant.schema_name):
                    # Criar o usuário comum
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    return redirect('success_url')  # Redirecionar para uma página de sucesso
            except Tenant.DoesNotExist:
                form.add_error('tenant_name', 'Tenant não encontrado.')
            except Exception as e:
                form.add_error(None, f'Erro ao criar usuário: {e}')
    else:
        form = CreateUserForm()

    return render(request, 'create_user.html', {'form': form})

class Homepage(FormView):
    template_name = 'homepage.html'
    form_class = FormHomePage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated: #usuario autenticado
            return redirect('gestao:homegestor') #redireciona
        else:
            return super().get(request, *args, **kwargs) #redireciona para homepage
        
def configuracao_view(request):
    configuracao_instance = get_object_or_404(configuracao, pk=1)

    if request.method == 'POST':
        form = ConfiguracaoForm(request.POST, instance=configuracao_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Configuração atualizada com sucesso!")
        else:
            messages.error(request, "Corrija os erros abaixo.")
    else:
        form = ConfiguracaoForm(instance=configuracao_instance)

    return render(request, 'configuracao.html', {'form': form})
     
class IntegracaoListView(LoginRequiredMixin, ListView):
    template_name = 'integracao.html'
    model = integracao
    context_object_name = 'integracoes'

class IntegracaoCreateView(CreateView):
    model = integracao
    form_class = FormIntegracao
    template_name = 'criar_integracao.html'

    def get_success_url(self):
        integracao_id = self.object.id
        state_uuid = uuid.uuid4().hex
        tenant_id = self.request.tenant.id
        state = f"{state_uuid}:{integracao_id}:{tenant_id}"

        return reverse_lazy('gestao:authorize') + f'?state={state}'

class IntegracaoDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'integracao_confirm_delete.html'
    model = integracao
    context_object_name = 'integracoes'

    def get_success_url(self):
        return reverse('gestao:integracao_list')

def authorize(request):
        state = request.GET.get('state')
        client_id = '439873324573602'
        redirect_uri = 'https://www.gestorem.com.br/callback'
        auth_url = f'https://auth.mercadolivre.com.br/authorization?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state={state}'
        return redirect(auth_url)
    
@csrf_exempt
def callback(request):
    if request.method == 'GET':
        data = request.GET.dict()  # Recebe os dados da query string
        
        expected_fields = {
            'code': str,
            'state': str
        }

        # Verifique se todos os campos esperados estão presentes e são do tipo correto
        for field, field_type in expected_fields.items():
            if field not in data or not isinstance(data[field], field_type):
                return JsonResponse({'status': 'error', 'message': f'Campo {field} faltando ou tipo invalido'}, status=400)

        # Extraia e processe os campos
        code = data['code']
        state = data['state']
        
        state = state.replace('%A3',":")
        state_uuid, integracao_id,tenant_id = state.split(':')

        tenant = get_object_or_404(Tenant, id = tenant_id)

        with schema_context(tenant.schema_name):
            integracao_vigente = get_object_or_404(integracao,id=integracao_id)

            url = 'https://api.mercadolibre.com/oauth/token'

            payload = {
                        'grant_type':'authorization_code',
                        'client_id':'439873324573602',
                        'client_secret':'kEy7ah8JxBVHnk3efd9LoSrpodZgc4CH',
                        'code':str(code),
                        'redirect_uri':'https://www.gestorem.com.br/callback',
                        'code_verifier':str(state)
                    }

            headers = {
                        'accept': 'application/json',
                        'Content-Type': 'application/x-www-form-urlencoded'
                        
                    }

            response = requests.post(url, data=payload, headers=headers)

            res = response.json()

            access_token = res.get('access_token')
            user_id = res.get('user_id')
            refresh_token = res.get('refresh_token')
            
            MeliAuth = MercadoLivreAuth(
                integracao =integracao_vigente,
                auth_code=user_id,
                access_token=refresh_token
            )

            integracao_vigente.id_seller = user_id

            MeliAuth.save()
            integracao_vigente.save()

            return redirect('gestao:integracao_list')
    
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)

## api meli
class get_refresh_token(View):
    def get(self, request, *args, **kwargs):
        try:
            url = 'https://api.mercadolibre.com/oauth/token'
            body = {
                'grant_type': 'refresh_token',
                'client_id': '439873324573602',
                'client_secret': 'kEy7ah8JxBVHnk3efd9LoSrpodZgc4CH',
                'refresh_token': MercadoLivreAuth.objects.first().access_token
            }

            response = requests.post(url, data=body)

            if response.status_code != 200:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Failed to get access token',
                    'details': response.json()
                }, status=response.status_code)

            data = response.json()
            return JsonResponse(data)

        except Exception as error:
            return JsonResponse({
                'status': 'error',
                'message': 'Error in get_refresh_token',
                'details': str(error)
            }, status=500)

#precificação
class get_price_info(View):
    def get(self, request, *args, **kwargs):
            return JsonResponse({
                'status': 'error',
                'message': 'Method GET not allowed. Use POST to update price.',
            }, status=405)

    def post(self, request, *args, **kwargs):
            try:

                refresh_token_url = request.build_absolute_uri('/api/refresh_token/')

                
                response = requests.get(refresh_token_url)
                
                if response.status_code != 200:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Failed to get refresh token',
                        'details': response.json()
                    }, status=response.status_code)
                
                data = response.json()
                access_token = data.get('access_token')

                if not access_token:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'No access token found in response',
                        'details': data
                    }, status=400)
                
                price = request.POST.get('price')
                mlb= request.POST.get('mlb')

                if not price:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Price not provided',
                    }, status=400)
                
                body = {
                    "price": price,
                }

                url = f'https://api.mercadolibre.com/items/{mlb}'  # Atualize o ID do item conforme necessário
                headers = {
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }

                response = requests.put(url, headers=headers, data=json.dumps(body))

                if response.status_code != 200:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Failed to update price info',
                        'details': response.json()
                    }, status=response.status_code)
                
                userdata = response.json()

                return JsonResponse(userdata)
            
            except Exception as error:
                print('Error in get user:', error)
                return JsonResponse({
                    'status': 'error',
                    'message': 'An error occurred',
                    'details': str(error)
                }, status=500)

#publicar anuncio
@method_decorator(csrf_exempt, name='dispatch')
class get_create_product(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'create_product.html')

    def post(self, request, *args, **kwargs):
        try:
            refresh_token_url = 'http://localhost:8000/api/refresh_token/'
            response = requests.get(refresh_token_url)
            
            if response.status_code != 200:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Failed to get refresh token',
                    'details': response.json()
                }, status=response.status_code)
            
            data = response.json()
            access_token = data.get('access_token')
            
            if not access_token:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No access token found in response',
                    'details': data
                }, status=400)
            
            # Parâmetros do produto
            product_data = {
                "title": request.POST.get('title'),
                "category_id": request.POST.get('category_id'),
                "price": request.POST.get('price'),
                "currency_id": request.POST.get('currency_id'),
                "available_quantity": request.POST.get('available_quantity'),
                "buying_mode": request.POST.get('buying_mode'),
                "condition": request.POST.get('condition'),
                "listing_type_id": request.POST.get('listing_type_id'),
                "pictures": [
                    {
                        "source": request.POST.get('picture_url')
                    }
                ],
                "attributes": [
                    {
                        "id": "BRAND",
                        "value_name": request.POST.get('brand')
                    },
                    {
                        "id": "EAN",
                        "value_name": request.POST.get('ean')
                    }
                ]
            }

            url = 'https://api.mercadolibre.com/items'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            response = requests.post(url, headers=headers, data=json.dumps(product_data))
            
            if response.status_code != 201:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Failed to create product',
                    'details': response.json()
                }, status=response.status_code)
            
            product_response_data = response.json()

            return JsonResponse(product_response_data)
        
        except Exception as error:
            print('Error in create product:', error)
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred',
                'details': str(error)
            }, status=500)       

class get_anuncios(View):
    def get(self, request, *args, **kwargs):
        try:
            # Obter o token de acesso
            refresh_token_url = request.build_absolute_uri('/api/refresh_token/')
            response = requests.get(refresh_token_url)
            
            if response.status_code != 200:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Failed to get refresh token',
                    'details': response.json()
                }, status=response.status_code)
            
            data = response.json()
            access_token = data.get('access_token')

            if not access_token:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No access token found in response',
                    'details': data
                }, status=400)

            def fetch_anuncios(scroll_id=None):
                url = 'https://api.mercadolibre.com/users/237330330/items/search?search_type=scan'
                if scroll_id:
                    url += f'&scroll_id={scroll_id}'

                headers = {
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }

                response = requests.get(url, headers=headers)

                if response.status_code != 200:
                    return {
                        'status': 'error',
                        'message': 'Failed to fetch anuncios',
                        'details': response.json()
                    }

                userdata = response.json()
                
                # Acumular os resultados
                current_results = userdata.get('results', [])
                next_scroll_id = userdata.get('scroll_id')

                if next_scroll_id:
                    next_results = fetch_anuncios(next_scroll_id)
                    current_results.extend(next_results)

                return current_results

            def process_results(results):
                detailed_results = []

                for item_id in results:
                    # Faça uma consulta à API para cada item_id
                    item_detail_url = f'https://api.mercadolibre.com/items/{item_id}'
                    headers = {
                        'Authorization': f'Bearer {access_token}',
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    }
                    item_response = requests.get(item_detail_url, headers=headers)

                    if item_response.status_code == 200:

                        data_detailed_item = item_response.json()

                        data_save_detailed_item_shipping =  data_detailed_item.get('shipping')

                        Anuncios = MercadoLivreAnuncios(
                            id_anuncio      = data_detailed_item.get('id'),
                            auth_code       =  data_detailed_item.get('seller_id'),
                            status          =  data_detailed_item.get('status'),
                            titulo          = data_detailed_item.get('title'),
                            price           =  data_detailed_item.get('price'),
                            category_id     = data_detailed_item.get('category_id'),
                            base_price      =  data_detailed_item.get('base_price'),
                            permalink       = data_detailed_item.get('permalink'),
                            thumbnail       = data_detailed_item.get('thumbnail'),
                            shipping_mode   = data_save_detailed_item_shipping.get('mode'),
                            shipping_free   =  data_save_detailed_item_shipping.get('free_shipping'),
                            shipping_logistic_type =  data_save_detailed_item_shipping.get('logistic_type')
                        )

                        Anuncios.save()

                    else:
                        print(f'Failed to fetch details for item {item_id}')
                
                return detailed_results

            # Primeiro, obtém todos os resultados
            all_results = fetch_anuncios()

            # Depois, processa os resultados
            all_detailed_results = process_results(all_results)

            return JsonResponse({'results': all_detailed_results})

        except Exception as error:
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred',
                'details': str(error)
            }, status=500)

class MercadoLivreAnuncios(LoginRequiredMixin, ListView):
    template_name = 'mercadolivre_anuncios.html'
    model = MercadoLivreAnuncios
    context_object_name = 'mercadoLivreanuncios_list'
    paginate_by = 20 
