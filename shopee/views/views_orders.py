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

def create_product(request):
        

        ShoppeAuth = models.ShopeeAuth.objects.first()
        partner_id = 1186920
        tmp = "4e7766654b516c73526e794545696a466d46525942784e44566977525050766b" # partner_key de teste, precisa trocar 

        timest = int(time.time())
        host = "https://partner.test-stable.shopeemobile.com"
        path = "/api/v2/product/add_item"

        shop_id = ShoppeAuth.shop_id
        access_token = ShoppeAuth.access_token

        tmp_base_string = "%s%s%s%s%s" % (partner_id, path, timest,access_token,shop_id)
        base_string = tmp_base_string.encode()
        partner_key = tmp.encode()
        sign = hmac.new(partner_key,base_string, hashlib.sha256).hexdigest()

        url = host + path + "?partner_id=%s&timestamp=%s&access_token=%s&shop_id=%s&sign=%s" % (partner_id, timest,access_token,shop_id,sign)

        payload=json.dumps({
            "attribute_list": [
            {
            "attribute_id": 4990,
            "attribute_value_list": [
                {
                "original_value_name": "Brand",
                "value_id": 32142,
                "value_unit": " kg"
                }
            ]
            }
        ],
        "brand": {
            "brand_id": 0,
            "original_brand_name": "nike"
        },
        "category_id": 102087,
        "condition": "NEW",
        "description": "item description test",
        "description_info": {
            "extended_description": {
            "field_list": [
                {
                "field_type": "image",
                "image_info": {
                    "image_id": "sg-11134201-7r98o-lzepamyq23vd85"
                    }
                }
            ]
            }
        },
        "description_type": "normal",
        "dimension": {
            "package_height": 11,
            "package_length": 11,
            "package_width": 11
        },
        "image": {
            "image_id_list": [
            "-"
            ]
        },
        "item_dangerous": 0,
        "item_name": "Item Name Example",
        "item_sku": "-",
        "item_status": "UNLIST",
        "logistic_info": [
            {
            "enabled": True,
            "logistic_id": 80101,
            }
        ],
        "normal_stock": 33,
        "original_price": 0,
        "pre_order": {
            "days_to_ship": 0,
            "is_pre_order": True
        },
        "seller_stock": [
            {
            "location_id": "BR",
            "stock": 0
            }
        ],
        "weight": 0.1
            })


        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("POST",url,headers=headers, data=payload, allow_redirects=False)
        res = response.json()

        return JsonResponse(res)