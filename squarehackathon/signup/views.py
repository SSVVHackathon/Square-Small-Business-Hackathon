from django.shortcuts import render, redirect
from .forms import signupForm
from django.contrib.auth import login, authenticate
from main.models import *
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def signup_view(request):
    form = signupForm(request.POST) 
    if form.is_valid():
        form.save()
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=password)
        login(request, user)
        print(request.user, user.name, user.email)
        Customer.objects.create(user.name)
        return redirect('home')
    else:
        form = signupForm()

    
    return render(request, 'signup.html', {'form': form})
