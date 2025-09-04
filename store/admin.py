from django.contrib import admin
from .models import Product, Variations


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'is_available', 'modified_date')
    list_display_links = ('name',)
    

class VariationsAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'created_date')
    list_display_links = ('product',)
    list_editable = ('is_active',)
    list_filter = ('variation_category', 'variation_value', 'is_active')
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Variations, VariationsAdmin)