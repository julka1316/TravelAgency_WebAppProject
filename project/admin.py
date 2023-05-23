from django.contrib import admin
from project.models import Customer, Trip, Transaction, TransactionItem
# Register your models here.

admin.site.register(Customer)
admin.site.register(Trip)
admin.site.register(Transaction)
admin.site.register(TransactionItem)
