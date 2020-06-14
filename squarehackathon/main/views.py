from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *
from signup.models import *

# Create your views here.
def home(request):
    context = {}
    return render(request, "home.html", context)

def process_payment(request):
    data = json.loads(request.body)
    nonce = data['nonce']
    print(nonce)