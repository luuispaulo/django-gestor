#from django.shortcuts import render
from typing import Any
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

