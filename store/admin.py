from django.contrib import admin
from .models import Product, Category, Customer, Order


class adminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'Category']


class adminCategory(admin.ModelAdmin):
    list_display = ['name',]

class adminCustomer(admin.ModelAdmin):
    list_display = ['first_name','last_name','phone','email','password']


admin.site.register(Product, adminProduct)
admin.site.register(Category, adminCategory)
admin.site.register(Customer, adminCustomer)
admin.site.register(Order)

