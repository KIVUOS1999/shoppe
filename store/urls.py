from django.urls import path
from . import views


urlpatterns= [
	path("",views.home, name= 'home'),
	path("login/", views.login_page, name = 'login'),
	path("cart/", views.cart, name= 'cart'),
	path("updatecart/", views.updatecart, name = 'updatecart'),
	path("checkout/", views.checkout, name = 'checkout'),
	path("proceedToPayment/", views.proceedToPayment, name = "proceedToPayment")
]