

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
	custmer_id=models.AutoField(primary_key=True)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
	 	return self.name

class Group(models.Model):
	group_id=models.AutoField(primary_key=True)
	group_name=models.CharField(max_length=200,null=True)


class Expense(models.Model):
	group_id=models.ForeignKey(Group,on_delete=models.CASCADE)
	items=models.CharField(max_length=200,null=False)
	paid_by=models.ForeignKey(Customer,on_delete=models.CASCADE)
	price=models.IntegerField(null=True)

class BalanceTable(models.Model):
	userName= models.OneToOneField(Customer)
	customer_id=models.ForeignKey(Customer,on_delete=models.CASCADE)
	balance=models.IntegerField(null=True)
	

