# forms.py
from django import forms
from .models import configuracao, integracao

class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    tenant_name = forms.CharField(max_length=50)

class FormHomePage(forms.Form):
    email = forms.EmailField(label=False)

### adição configuracao.html##
class ConfiguracaoForm(forms.ModelForm):
    class Meta:
        model = configuracao
        fields = ['imposto', 'embalagem', 'publicidade', 'transporte', 'custofixo', 'lucratividade']

class MeliFilterForm(forms.Form):
    id_venda = forms.CharField(required=False, label='ID Venda')
    titulo_anuncio = forms.CharField(required=False, label='Título')

class FormIntegracao(forms.ModelForm):
    MARKETPLACE_CHOICES = [
        (1,'Mercado Livre'),
    ]

    id_marketplace = forms.ChoiceField(choices=MARKETPLACE_CHOICES)

    class Meta:
        model = integracao
        fields = ['name','id_marketplace']