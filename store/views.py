from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json

def home(request):
	return render(request, "store/store.html", {'products':Product.objects.all()})

def login_page(request):
	return render(request, "store/login_page.html", {})

def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer = customer, completed = False)
		items = order.orderitem_set.all()
	else:
		items = []

	return render(request, "store/cart.html", {'items':items, 'order':order})

def updatecart(request):
	data = json.loads(request.body)
	productID = data['productID']
	product=Product.objects.get(id=productID)
	action = data['action']
	customer = request.user.customer

	order, created = Order.objects.get_or_create(customer=customer, completed=False)
	orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action=='add':
		orderitem.quantity+=1
	elif action=='remove':
		orderitem.quantity-=1

	orderitem.save()

	if orderitem.quantity <= 0:
		orderitem.delete()
	
	return JsonResponse("Item added", safe = False)


def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer = customer, completed = False)
		items = order.orderitem_set.all()
	else:
		items = []
	return render(request, 'store/checkout.html', {'items':items, 'order':order})