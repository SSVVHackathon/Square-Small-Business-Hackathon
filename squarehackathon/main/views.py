from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *
from signup.models import *

# Create your views here.
def home(request):
    context = {}
    return render(request, "home.html", context)

@csrf_exempt
def process_payment(request):
    data = json.loads(request.body)
    nonce = data['nonce']
    print(nonce)

    return JsonResponse('Item was added', safe=False)

