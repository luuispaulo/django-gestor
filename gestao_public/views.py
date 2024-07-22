from .models import Tenant, Domain
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from .forms import CriarContaForm, FormHomePage
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from .models import relatorio

# Create your views here.

class Homepage(FormView):
    template_name = 'homepage.html'
    form_class = FormHomePage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated: #usuario autenticado
            return redirect('gestao:homegestor') #redireciona
        else:
            return super().get(request, *args, **kwargs) #redireciona para homepage

    def get_success_url(self):
        username = self.request.POST.get("username")
        usuarios = User.objects.filter(username=username)
        if usuarios:
            return f"http://{username}.gestorem.com.br/login"
        else:
            return reverse('gestao_public:criarconta')
        
class Criarconta(FormView):
    template_name = 'criarconta.html'
    form_class = CriarContaForm

    def form_valid(self, form):
        # Salva o usuário
        user = form.save()

        # Cria o tenant
        tenant = Tenant(
            schema_name=user.username,  
            name=user.username,
        )
        tenant.save()

        # Cria o domínio para o tenant
        domain = Domain(
            domain=f'{user.username}.gestorem.com.br',
            tenant=tenant
        )
        domain.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('gestao_public:homepage')