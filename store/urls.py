from django.urls import path
from . import views

urlpatterns= [
	path("",views.home, name= 'home'),
	path("login/", views.login_page, name = 'login'),
	path("register/", views.register_page, name = 'register'),
	path("cart/", views.cart, name= 'cart'),
	path("updatecart/", views.updatecart, name = 'updatecart'),
	path("checkout/", views.checkout, name = 'checkout'),
	path("proceedToPayment/", views.proceedToPayment, name = "proceedToPayment"),
	path("trans_register_page/", views.trans_register_page, name = "trans_register_page")
]