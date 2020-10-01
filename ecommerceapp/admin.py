from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Customer)
#@admin.register(Category)
#class CategoryAdmin(admin.ModelAdmin):
    #list_display = ['name', 'slug']
    #prepopulated_fields = { 'slug': ('name', )}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = { 'slug': ('product_name', )}


@admin.register(Order)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['customer', 'date_ordered', 'complete',]
    list_editable = ['complete']

@admin.register(OrderItem)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'quantity']
    list_filter = ['product', 'order']
    list_editable = ['quantity']
