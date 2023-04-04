from django.db import models
from category.models import Category,Brand
from django.urls import reverse
from django.utils.text import slugify
from accounts.models import Account

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    images = models.ImageField(upload_to='products')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    description = models.TextField(max_length=500,blank=True)
    is_available = models.BooleanField(default=True)  
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    price = models.PositiveBigIntegerField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug ])

    def __str__(self):
        return self.product_name
    

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    imagess = models.ImageField(upload_to='product-imagess')
     
# ------------ variations -----------------

class Color(models.Model):
    color = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.color
    
class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    

    def __str__(self):
        return self.color.color
    



# Class ReviewRate Model
class ReviewRating(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    image = models.ImageField(upload_to='productreview', blank=True)
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        
        return self.subject







