from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

import hmac
import json
import time
import requests
import hashlib

# Este codigo é projetado apra autenticação de contas shop e nao main_accounts, caso algum conflito, necessário corrigir para atender aos dois caminhos
# segue documentação https://open.shopee.com/developer-guide/20

#Função de redirecionamento para autenticação
def authorize_shopee(request):
        partner_id = 1186920 # partner_id de teste, precisa trocar 
        tmp = "4e7766654b516c73526e794545696a466d46525942784e44566977525050766b" # partner_key de teste, precisa trocar 

        
        host = "https://partner.test-stable.shopeemobile.com"
        path = "/api/v2/shop/auth_partner"
        redirect_url = "https://www.gestorem.com.br/"
        
        timest = int(time.time())
        partner_key = tmp.encode()
        tmp_base_string = "%s%s%s" % (partner_id, path, timest)
        base_string = tmp_base_string.encode()
        sign = hmac.new(partner_key, base_string, hashlib.sha256).hexdigest()

        url = host + path + "?partner_id=%s&timestamp=%s&sign=%s&redirect=%s" % (partner_id, timest, sign, redirect_url)

        return redirect(url)

@csrf_exempt
def callback_shopee(request):
    if request.method == 'GET':
        data = request.GET.dict()  # Recebe os dados da query string
        
        expected_fields = {
            'code': str,
            'shop_id': str
        }

        # Verifique se todos os campos esperados estão presentes e são do tipo correto
        for field, field_type in expected_fields.items():
            if field not in data or not isinstance(data[field], field_type):
                return JsonResponse({'status': 'error', 'message': f'Campo {field} faltando ou tipo invalido'}, status=400)

        # Extraia e processe os campos
        code = data['code']
        shop_id = int(data['shop_id'])

        partner_id = 1186920
        tmp = "4e7766654b516c73526e794545696a466d46525942784e44566977525050766b" # partner_key de teste, precisa trocar 

        timest = int(time.time())
        host = "https://partner.test-stable.shopeemobile.com"
        path = "/api/v2/auth/token/get"
        body = {"code": code, "shop_id": shop_id, "partner_id": partner_id}
        tmp_base_string = "%s%s%s" % (partner_id, path, timest)
        base_string = tmp_base_string.encode()
        partner_key = tmp.encode()
        sign = hmac.new(partner_key, base_string, hashlib.sha256).hexdigest()
        url = host + path + "?partner_id=%s&timestamp=%s&sign=%s" % (partner_id, timest, sign)
        # print(url)
        headers = {"Content-Type": "application/json"}
        resp = requests.post(url, json=body, headers=headers)
        ret = json.loads(resp.content)
        access_token = ret.get("access_token")
        new_refresh_token = ret.get("refresh_token")


        return JsonResponse({
             'status': 'success', 
             'message': {
                  'data':data,
                  'code':code,
                  'shop_id':shop_id,
                  'ret': ret
                  },
                  }, status=200)
