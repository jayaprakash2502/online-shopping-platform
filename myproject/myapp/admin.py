from django.contrib import admin
from .models import customer, category, products


@admin.register(customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone']
    actions = ['delete_selected']


@admin.register(category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name']
    actions = ['delete_selected']


@admin.register(products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'price', 'category', 'description']
    actions = ['delete_selected']
