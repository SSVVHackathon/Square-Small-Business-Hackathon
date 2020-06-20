from django import forms
from .admin import UserCreationForm
from .models import MyUser

class signupForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('email', 'name', 'password1', 'password2')