from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    cat_name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    description = models.TextField(max_length=255,blank=True)
    cat_image = models.ImageField(upload_to='categories',blank=True)

    class Meta():
        verbose_name = ('category')
        verbose_name_plural = ('categories')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.cat_name)
        super(Category,self).save(*args, **kwargs)

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.cat_name

class Brand(models.Model):
    brand_name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=100,unique=True)

    def get_url(self):
        return reverse('products_by_brand', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.brand_name)
        super(Brand,self).save(*args, **kwargs)

    def __str__(self):
        return self.brand_name
        