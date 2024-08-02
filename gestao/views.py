from django.shortcuts import render, redirect, reverse, get_object_or_404
from typing import Any
from django.db.models.query import QuerySet
from .models import relatorio, meli_237330330, configuracao,MercadoLivreAuth,integracao 
from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView,CreateView
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

# Create your views here.
#def homepage(request):
#   return render(request, 'homepage.html')

##substitui a função por uma classe pre definida

#lista de filmes na view homegestor
#def homegestor(request):
#   context = {}
#    lista_relatorios = relatorio.objects.all()
#    context['lista_relatorios'] = lista_relatorios
#    return render(request, 'homegestor.html',context)

class Homegestor(LoginRequiredMixin, ListView):
    template_name = 'homegestor.html'
    model = meli_237330330
    context_object_name = 'meli_237330330_list'
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
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
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
        
## adição configuracao.html ##

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

        state = f"{state_uuid}:{integracao_id}"

        return reverse_lazy('gestao:authorize') + f'?state={state}'

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
        state_uuid, integracao_id = state.split(':',1)

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
                user = request.user,
                auth_code = user_id,
                access_token = refresh_token
        )

        integracao_vigente.id_seller = user_id

        MeliAuth.save()
        integracao_vigente.save()

        return redirect("gestao:homegestor")
    
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)