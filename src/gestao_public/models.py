from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Tenant(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)

    auto_create_schema = True

class Domain(DomainMixin):
    pass

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
