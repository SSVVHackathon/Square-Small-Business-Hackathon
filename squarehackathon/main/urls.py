from django.urls import path, include
from signup import views as signup_views
from payment import views as payment_views
from .views import *

urlpatterns = [
    path('process-payment', process_payment, name="process-payment"),
    path('signup', signup_views.signup_view, name="signup"),
    path('', home, name="home"),
    path('checkout', payment_views.checkout, name="checkout"),
    path('', include("django.contrib.auth.urls")),
    path('order', order, name="order"),
    path('create-order', create_order, name="create_order")
]