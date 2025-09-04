from django.db import models
from core.utils import unique_slug_generator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=75, unique=True)
    slug = models.SlugField(max_length=125, unique=True, blank=True)
    description = models.TextField()
    category_image = models.ImageField(upload_to='categories', blank=True)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        
    def get_url(self):
        return reverse('product_by_cateogry', args=[self.slug])

    def __str__(self):
        return self.name
    
# Automatic slug
@receiver(pre_save, sender = Category)
def pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        print(f"Model: {instance.slug}")
        instance.slug = unique_slug_generator(instance)
    
