from django.shortcuts import render, redirect, reverse
from typing import Any
from django.db.models.query import QuerySet
from .models import relatorio, meli_237330330
from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tenants.utils import schema_context
from gestao_public.models import Tenant
from .forms import CreateUserForm, FormHomePage

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

class Homegestor(LoginRequiredMixin,ListView):
    template_name = 'homegestor.html'
    model = relatorio

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