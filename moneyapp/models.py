from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
# Create your models here.
#Customer tables has all the details of the registered
class Customer(models.Model):
	custmer_id=models.AutoField(primary_key=True)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
	 	return self.name



class Expense(models.Model):

	expense_id =models.AutoField(primary_key=True)
	item = models.CharField(max_length=200,null=True)
	author_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
	Bill_Date=models.DateField(auto_now_add=True,null=True)
	no_of_splits=models.IntegerField(null=True)
	split_members= ArrayField(ArrayField(models.IntegerField(null=True)))
	paid = models.BooleanField(default=False)
	amount=models.IntegerField(null=True)

class Expense_Split(models.Model):
	split_id = models.AutoField(primary_key=True)
	expense_id= models.ForeignKey(Expense,on_delete=models.CASCADE)
	split_amount=models.IntegerField(null=True)
	reciept_id= models.ForeignKey(Customer,on_delete=models.CASCADE)
	reciept_paid=models.BooleanField(default=False)