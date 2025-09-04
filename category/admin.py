from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'category_image']
    list_display_links = ['name']
    
    
admin.site.register(Category, CategoryAdmin)