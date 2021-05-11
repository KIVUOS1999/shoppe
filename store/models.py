from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank = True, on_delete=models.CASCADE)
	name = models.CharField(max_length = 200, null = True)
	email = models.CharField(max_length = 200, null = True)


	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length = 200, null = True)
	description = models.TextField()
	price = models.FloatField()
	image = models.ImageField(null = True, blank = True)

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url
	
	def __str__(self):
		return self.name


class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, blank = True)
	date_ordered = models.DateTimeField(auto_now_add = True)
	completed = models.BooleanField(default = False)
	transaction_id = models.CharField(max_length = 100, null = True)

	def __str__(self):
		return str(self.id)

	@property
	def total_items_in_cart(self):
		total_items = self.orderitem_set.all()
		return sum([i.quantity for i in total_items])

	@property
	def grand_total(self):
		total_items = self.orderitem_set.all()
		return sum([i.total for i in total_items])
	
	
	

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True, blank = True)
	order = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True, blank = True)
	quantity = models.IntegerField(default = 0)
	dateadded = models.DateTimeField(auto_now_add = True)

	@property
	def total(self):
		return self.quantity * self.product.price
	

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, blank = True)
	order = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True, blank = True)
	address = models.CharField(max_length = 200, null = True)
	city = models.CharField(max_length = 20, null = True)
	state = models.CharField(max_length = 20, null = True)
	zip_code = models.CharField(max_length = 20, null = True)
	dateadded = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.address

