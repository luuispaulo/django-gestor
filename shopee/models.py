from django.db import models
from gestao import models as gestao_models
# Create your models here.

class ShopeeAuth(models.Model):
    integracao = models.ForeignKey(gestao_models.integracao, on_delete=models.CASCADE)
    shop_id = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.integracao.name} - {self.auth_code}'