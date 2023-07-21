import datetime as dt

from django.db import models
from django.db.models import Sum, F


class Employee(models.Model):
    full_name = models.CharField(max_length=200)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.full_name


class Client(models.Model):
    full_name = models.CharField(max_length=200)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.full_name


class Product(models.Model):
    name = models.CharField(max_length=500, unique=True)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return self.name


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.product.name} (x{self.quantity})"


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, related_name='orders')
    products = models.ManyToManyField(ProductOrder)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='orders')
     
    date = models.DateField(default=dt.date.today)

    def price(self):
        total_amount = self.products.aggregate(
            total_amount=Sum(F('quantity') * F('product__price'))
        )['total_amount']

        total_amount = total_amount or 0.0

        return f"${total_amount}"
    
    def __str__(self) -> str:
        return f"{self.client} [{self.employee}] {self.price()}"
