from django.urls import path, include
from signup import views as signup_views
from payment import views as payment_views
from .views import *

urlpatterns = [
    path('checkout/process-payment/', process_payment, name="process-payment"),
    path('signup/', signup_views.signup_view, name="signup"),
    path('', home, name="home"),
    path('checkout/', checkout, name="checkout"),
    path('payment/', payment_views.payment, name="payment"),
    path('contactus/', contact, name='contact'),
    path('', include("django.contrib.auth.urls")),
    path('order', order, name="order"),
    path('update_item/', updateItem, name="update_item"),
	path('process_order/', processOrder, name="process_order"),
    path('cart/', cart, name="cart")
]