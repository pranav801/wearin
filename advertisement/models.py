from django.db import models
from category.models import Brand
# Create your models here.

class Advertisement(models.Model):
    ad_name = models.CharField(max_length=255)
    ad_image = models.ImageField(upload_to='ad_image')
    ad_description = models.CharField(max_length=255)
    ad_brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.ad_name