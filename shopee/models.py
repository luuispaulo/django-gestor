from django.db import models
from django.utils import timezone
from gestao import models as gestao_models
# Create your models here.

class ShopeeAuth(models.Model):
    shop_id = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.auth_code}'
    
class SessionIntegration(models.Model):
    tenant_id = models.IntegerField()
    session_key = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='pendente')

    def is_expired(self):
        # Supondo que as sessões expiram em 10 minutos
        return timezone.now() > self.created_at + timezone.timedelta(minutes=10)
