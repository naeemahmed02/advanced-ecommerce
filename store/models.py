from django.db import models
from category.models import Category
from core.utils import unique_slug_generator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse

class Product(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    slug = models.SlugField(max_length=1200, unique=True, blank=True)
    product_description = models.TextField(blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='products', blank=True)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tax = models.DecimalField(default=2.0, decimal_places=2, max_digits=100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        
    # def tax(self):
    #     return (self.tax * self.price) / 100
        
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
        
    
    def __str__(self):
        return self.name
    
variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variations(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Variation'
        verbose_name_plural = 'Variations'
        
    
    def __str__(self):
        return self.variation_value
    
# Automatic slug
@receiver(pre_save, sender = Product)
def pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        print(f"Model: {instance.slug}")
        instance.slug = unique_slug_generator(instance)