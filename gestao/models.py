from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class meli_237330330(models.Model):
    id_venda = models.CharField(max_length=200, primary_key=True) 
    status = models.CharField(max_length=200)
    data_de_criacao = models.DateTimeField(default=timezone.now)
    valor_pedido = models.DecimalField(max_digits=10, decimal_places=2)
    comissao_taxa_fixa = models.DecimalField(max_digits=10, decimal_places=2)
    frete_cobrado = models.DecimalField(max_digits=10, decimal_places=2)
    repasse = models.DecimalField(max_digits=10, decimal_places=2)
    mlb = models.CharField(max_length=500)
    titulo_anuncio = models.TextField()
    sku = models.CharField(max_length=500)
    quantidade = models.IntegerField()
    modo_de_envio = models.CharField(max_length=200)

    class Meta:
        db_table = 'meli_237330330'
        managed = False

    def __str__(self):
        return self.titulo_anuncio

LISTA_SETORES = (
    ("COMPRAS", "Compras"),
    ("FINANCEIRO", "Financeiro"),
    ("LOGISTICA", "Logística"),
    ("COMERCIAL", "Comercial"),
    ("RH", "RH"),
    ("DIRETORIA", "Diretoria")
)

class relatorio(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    setor = models.CharField(max_length=20, choices=LISTA_SETORES)
    src = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.nome

## adição configuracao.html ###


class configuracao(models.Model):
    id = models.AutoField(primary_key=True)
    imposto = models.FloatField(blank=True, null=True, default=1)
    embalagem = models.FloatField(blank=True, null=True, default=1)
    publicidade = models.FloatField(blank=True, null=True, default=1)
    transporte = models.FloatField(blank=True, null=True, default=1)
    custofixo = models.FloatField(blank=True, null=True, default=1)
    CMV = models.FloatField(blank=True, null=True, default=1)
    data = models.DateTimeField(default=timezone.now)

def __str__(self):
        return f"Configuração {self.pk}"

class integracao(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image_src = models.TextField()
    name = models.CharField(max_length=50)
    is_activate = models.BooleanField(default=True)
    id_marketplace = models.IntegerField()
    id_seller = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'gestao_integracao'

class MercadoLivreAuth(models.Model):
    integracao = models.ForeignKey(integracao, on_delete=models.CASCADE)
    auth_code = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.integracao.name} - {self.auth_code}'

class Orders(models.Model):
    integracao = models.ForeignKey(integracao, on_delete=models.CASCADE)
    id_venda = models.CharField(max_length=200, primary_key=True) 
    status = models.CharField(max_length=200)
    data_de_criacao = models.DateTimeField(default=timezone.now)
    valor_pedido = models.DecimalField(max_digits=10, decimal_places=2)
    comissao_taxa_fixa = models.DecimalField(max_digits=10, decimal_places=2)
    frete_cobrado = models.DecimalField(max_digits=10, decimal_places=2)
    repasse = models.DecimalField(max_digits=10, decimal_places=2)
    id_anuncio = models.CharField(max_length=500)
    titulo_anuncio = models.TextField()
    sku = models.CharField(max_length=500)
    quantidade = models.IntegerField()
    modo_de_envio = models.CharField(max_length=200)

    def __str__(self):
        return self.id_venda
    
class MercadoLivreAnuncios(models.Model):
    id_anuncio = models.CharField(max_length=20,default ='')
    status = models.CharField(max_length=20,default ='')
    auth_code = models.CharField(max_length=20, default='default_auth_code_value')
    titulo = models.TextField(default ='')
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    base_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    category_id = models.CharField(max_length=20,default ='')
    permalink = models.CharField(max_length=500,default ='')
    thumbnail = models.CharField(max_length=500,default ='')
    shipping_mode = models.TextField(default ='')
    shipping_free = models.BooleanField(default =True)
    shipping_logistic_type = models.TextField(default ='')

    def __str__(self):
        return self.id_anuncio

