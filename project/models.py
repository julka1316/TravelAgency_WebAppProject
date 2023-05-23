from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Customer(models.Model):
    customername = models.CharField(max_length=50)
    surname = models.CharField(max_length=200)
    age = models.IntegerField()
    email = models.EmailField()

    def json(self):
        return {
            "id": self.id,
            "customername": self.customername,
            "surname": self.surname,
            "age": self.age,
            "email": self.email

        }

class Trip(models.Model):
    tripname = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    date_1 = models.DateField(blank=True, null=True)
    date_2 = models.DateField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(null = True, blank = True, upload_to="images/")

    def json(self):
        return {
            "id": self.id,
            "tripname": self.tripname,
            "description": self.description,
            "date_1": self.date_1,
            "date_2": self.date_2,
            "price": self.price
        }

class TransactionItem(models.Model):
    item = models.ForeignKey(Trip, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default="0")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

class Transaction(models.Model):
    date = models.DateTimeField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    items = models.ManyToManyField(TransactionItem, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def json(self):
        return {
            "id": self.id,
        }

