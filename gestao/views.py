#from django.shortcuts import render
from typing import Any

from django.db.models.query import QuerySet
from .models import relatorio
from django.views.generic import TemplateView, ListView, DetailView

# Create your views here.
#def homepage(request):
#   return render(request, 'homepage.html')

##substitui a função por uma classe pre definida
class Homepage(TemplateView):
    template_name = 'homepage.html'

#lista de filmes na view homegestor
#def homegestor(request):
#   context = {}
#    lista_relatorios = relatorio.objects.all()
#    context['lista_relatorios'] = lista_relatorios
#    return render(request, 'homegestor.html',context)

class Homegestor(ListView):
    template_name = 'homegestor.html'
    model = relatorio

class Dashboard(DetailView):
    template_name = 'dashboard.html'
    model = relatorio

    #object_list

class Pesquisagestao(ListView):
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