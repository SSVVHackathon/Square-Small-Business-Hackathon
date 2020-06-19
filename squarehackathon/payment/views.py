from django.shortcuts import render

# Create your views here.

def payment(request):
    context = {}
    return render(request, "payment.html", context)