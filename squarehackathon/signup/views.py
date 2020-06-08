from django.shortcuts import render, redirect
from .forms import signupForm
from django.contrib.auth import login, authenticate

def signup_view(request):
    form = signupForm(request.POST)
    if form.is_valid():
        form.save()
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=password)
        login(request, user)
        return redirect('home')
    else:
        form = signupForm()
    return render(request, 'signup.html', {'form': form})
