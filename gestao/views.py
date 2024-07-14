from django.shortcuts import render, redirect, reverse
from typing import Any
from django.db.models.query import QuerySet
from .models import relatorio
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CriarContaForm, FormHomePage

# Create your views here.
#def homepage(request):
#   return render(request, 'homepage.html')

##substitui a função por uma classe pre definida
class Homepage(FormView):
    template_name = 'homepage.html'
    form_class = FormHomePage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated: #usuario autenticado
            return redirect('gestao:homegestor') #redireciona
        else:
            return super().get(request, *args, **kwargs) #redireciona para homepage

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
        
class Perfil(LoginRequiredMixin,TemplateView):
    template_name = 'perfil.html'

class Criarconta(FormView):
    template_name = 'criarconta.html'
    form_class= CriarContaForm

## salvar forms
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

## redireciona o usuario apos criação da conta
    def get_success_url(self):
        return reverse ('gestao:login')