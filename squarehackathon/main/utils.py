import json
from .models import *
import datetime

def cartData(request):
    transaction_id = datetime.datetime.now().timestamp()
    if request.user.is_authenticated:
        customer = Customer.objects.get_or_create(user=request.user, name=request.user.name, email=request.user.email)
        order, created = Order.objects.get_or_create(transaction_id=transaction_id, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        return False
    return {'cartItems':cartItems, 'order':order, 'items':items}