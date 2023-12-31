from django.contrib import admin

from .models import *


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'price')
    list_editable = ('quantity', 'price')


@admin.register(ProductOrder)
class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')
    list_editable = ('quantity', )
    raw_id_fields = ('product', )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'employee', 'price', 'date')
    raw_id_fields = ('client', 'products')
