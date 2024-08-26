from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.utils.crypto import get_random_string
from django_tenants.utils import schema_context

from shopee import models
from gestao import models as gestao_models
from gestao_public import models as gestao_public_models

import requests
import hashlib
import hmac
import json
import time,datetime

# Este codigo é projetado apra autenticação de contas shop e nao main_accounts, caso algum conflito, necessário corrigir para atender aos dois caminhos
# segue documentação https://open.shopee.com/developer-guide/20

#Função de redirecionamento para autenticação
def authorize(request):
        
        data = request.GET.dict()

        state = data['state']

        # Partner_id,Partner_key e Host de teste, precisa trocar ( DADOS DO APLICATIVO DE INTEGRAÇÃO SHOPEE )
        partner_id = 1186920
        tmp = "4e7766654b516c73526e794545696a466d46525942784e44566977525050766b" 
        host = "https://partner.test-stable.shopeemobile.com"
        path = "/api/v2/shop/auth_partner"
        redirect_url = f"https://www.gestorem.com.br/shopee/auth/callback/?state={state}"
        
        # Codificação obrigatoria da shopee 
        timest = int(time.time())
        partner_key = tmp.encode()
        tmp_base_string = "%s%s%s" % (partner_id, path, timest)
        base_string = tmp_base_string.encode()
        sign = hmac.new(partner_key, base_string, hashlib.sha256).hexdigest()

        # Concatenando url string com parametros
        url = host + path + "?partner_id=%s&timestamp=%s&sign=%s&redirect=%s&code=123" % (partner_id, timest, sign, redirect_url)

        response = redirect(url)

        return response

@csrf_exempt
def callback(request):
    if request.method == 'GET':
        
        data = request.GET.dict()  # Recebe os dados da query string
        
        expected_fields = {
            'state':str,
            'code': str,
            'shop_id': str
        }

        # Verifique se todos os campos esperados estão presentes e são do tipo correto
        for field, field_type in expected_fields.items():
            if field not in data or not isinstance(data[field], field_type):
                return JsonResponse({'status': 'error', 'message': f'Campo {field} faltando ou tipo invalido'}, status=400)

        # Extraia e processe os campos
        state =  data['state']
        code = data['code']
        shop_id = int(data['shop_id'])
        
        state = state.replace('%A3',":")
        state_uuid, integracao_id,tenant_id = state.split(':')

        tenant = get_object_or_404(gestao_public_models.Tenant, id = tenant_id)

        with schema_context(tenant.schema_name):
            integracao_vigente = get_object_or_404(gestao_models.integracao,id=integracao_id)

            partner_id = 1186920
            tmp = "4e7766654b516c73526e794545696a466d46525942784e44566977525050766b" # partner_key de teste, precisa trocar 

            timest = int(time.time())
            host = "https://partner.test-stable.shopeemobile.com"
            path = "/api/v2/auth/token/get"

            tmp_base_string = "%s%s%s" % (partner_id, path, timest)
            base_string = tmp_base_string.encode()
            partner_key = tmp.encode()
            sign = hmac.new(partner_key, base_string, hashlib.sha256).hexdigest()

            url = host + path + "?partner_id=%s&timestamp=%s&sign=%s" % (partner_id, timest, sign)

            body = {
                "code": code,
                "shop_id": shop_id,
                "partner_id": partner_id
                }
                
            headers = {
                "Content-Type": "application/json"
                }
            
            resp = requests.post(url, json=body, headers=headers)
            res = json.loads(resp.content)

            access_token = res.get("access_token")
            refresh_token = res.get("refresh_token") 


            models.ShopeeAuth.objects.create(
                shop_id = shop_id,
                access_token = access_token,
                refresh_token = refresh_token
            )

            integracao_vigente.id_seller = shop_id
            integracao_vigente.save()
        return redirect('gestao:integracao_list')

def refresh_token(request):
        
        ShoppeAuth = models.ShopeeAuth.objects.first()
        partner_id = 1186920
        tmp = "4e7766654b516c73526e794545696a466d46525942784e44566977525050766b" # partner_key de teste, precisa trocar 

        timest = int(time.time())
        host = "https://partner.test-stable.shopeemobile.com"
        path = "/api/v2/auth/access_token/get"

        tmp_base_string = "%s%s%s" % (partner_id, path, timest)
        base_string = tmp_base_string.encode()
        partner_key = tmp.encode()
        sign = hmac.new(partner_key, base_string, hashlib.sha256).hexdigest()

        url = host + path + "?partner_id=%s&timestamp=%s&sign=%s" % (partner_id, timest, sign)

        body = {
            "shop_id": int(ShoppeAuth.shop_id),
            "refresh_token":ShoppeAuth.refresh_token,
            "partner_id": int(partner_id)
            }
            
        headers = {
            "Content-Type": "application/json"
            }
        
        resp = requests.post(url, json=body, headers=headers)
        res = json.loads(resp.content)

        ShoppeAuth.refresh_token = res.get('refresh_token')
        ShoppeAuth.access_token = res.get('access_token')
        ShoppeAuth.created_at = datetime.datetime.now()
        ShoppeAuth.save()

        return JsonResponse(res)