from django.urls import path, include
from signup.views import views as signup_views
from payment.views import views as payment_views
from .views import home

urlpatterns = [
    path('signup', signup_views.signup_view, name="signup"),
    path('', home, name="home"),
    path('checkout', payment_views.checkout, name="checkout"),
    path('process-payment', )
]