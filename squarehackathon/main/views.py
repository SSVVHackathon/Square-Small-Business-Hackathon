from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_protect
from .models import *
from signup.models import *
from square.client import Client
import uuid
from .utils import *
import datetime


# Create your views here.
def home(request):
    data = cartData(request=request)
    cartItems = data['cartItems']

    context = {'cartItems':cartItems, 'shipping':False}
    return render(request, "home.html", context)
def contact(request):
    return render(request,'maps.html')
def order(request):
    data = cartData(request=request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems, 'shipping':False}
    return render(request, "order.html", context)

def cart(request):
    data = cartData(request=request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'cart.html', context)

def checkout(request):
    data = cartData(request=request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems, 'shipping':False}
    return render(request, 'checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    order.location = data['location']['location']
    order.delivery = data['carryoutOrDelivery']['carryoutOrDelivery']
    order.address = data['shipping']['address']
    order.city = data['shipping']['city']
    order.state=data['shipping']['state']
    order.zipcode=data['shipping']['zipcode']
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    return JsonResponse('Payment Complete', safe=False)


@csrf_protect
def process_payment(request):
    data = json.loads(request.body)
    amountDue = data['amountDue']
    nonce = data['nonce']

    config_type = "SANDBOX"
    access_token = "EAAAELuuq-CJ1qho_UBpAJrWMlFmA0hTS3s4dKCJOeQa6WmZLsO7PTm-1K-HiGlc"

    client = Client(
        access_token=access_token,
        environment="sandbox",
    )

    idempotency_key = str(uuid.uuid1())

    amount = {'amount': amountDue, 'currency': 'USD'}

    body = {'idempotency_key': idempotency_key, 'source_id': nonce, 'amount_money': amount}

    api_response = client.payments.create_payment(body)
    if api_response.is_success():
        res = api_response.body['payment']
    elif api_response.is_error():
        res = "Exception when calling PaymentsApi->create_payment: {}".format(api_response.errors)

    
    return JsonResponse('Item was added', safe=False)
