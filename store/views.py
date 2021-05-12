from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime

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

def proceedToPayment(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer = customer, completed = False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id

		if(total == order.grand_total):
			order.completed = True

		order.save()

		ShippingAddress.objects.create(
			customer = customer,
			order = order,
			address = data['shipping']['address'],
			city = data['shipping']['city'],
			state = data['shipping']['state'],
			zip_code = data['shipping']['zipcode'],
		)

	else:
		print("User is not logged in")


	return JsonResponse({'message':"Proceed to payment"}, safe = False)

def register_page(request):
	return render(request, "store/register_page.html", {})

def trans_register_page(request):
	data = json.loads(request.body)
	usr = User.objects.create_user(
		data['registration_data']['username'],
		'',
		data['registration_data']['pass1'],
	)
	curr_user, created = Customer.objects.get_or_create(user = usr)
	curr_user.name = data['registration_data']['name']
	curr_user.email = data['registration_data']['email']

	curr_user.save()

	return JsonResponse('register_page', safe=False)
