from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_protect
from .models import *
from signup.models import *
from square.client import Client
import uuid
from .utils import cartData


# Create your views here.
def home(request):
    data = cartData(request=request)
    if not data:
        context = {'cartItems': False}
    else:
        cartItems = data['cartItems']
        print(cartItems)
        context = {}
    return render(request, "home.html", context)

def order(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, "order.html", context)

@csrf_protect
def process_payment(request):
    data = json.loads(request.body)
    nonce = data['nonce']

    config_type = "SANDBOX"
    access_token = "EAAAELuuq-CJ1qho_UBpAJrWMlFmA0hTS3s4dKCJOeQa6WmZLsO7PTm-1K-HiGlc"

    client = Client(
        access_token=access_token,
        environment="sandbox",
    )

    idempotency_key = str(uuid.uuid1())

    amount = {'amount': 100, 'currency': 'USD'}

    body = {'idempotency_key': idempotency_key, 'source_id': nonce, 'amount_money': amount}

    api_response = client.payments.create_payment(body)
    if api_response.is_success():
        res = api_response.body['payment']
    elif api_response.is_error():
        res = "Exception when calling PaymentsApi->create_payment: {}".format(api_response.errors)

    
    return JsonResponse('Item was added', safe=False)

@csrf_protect
def create_order(request):
    config_type = "SANDBOX"
    access_token = "EAAAELuuq-CJ1qho_UBpAJrWMlFmA0hTS3s4dKCJOeQa6WmZLsO7PTm-1K-HiGlc"

    client = Client(
        access_token=access_token,
        environment="sandbox",
    )

    idempotency_key = str(uuid.uuid1())

    location_id = "592Z9CJKVSCYB"

    body = {'idempotency_key': idempotency_key, 'location_id':location_id, 'body': 'hello'}

    order = client.orders.calculate_order(body)

