from django.contrib import admin
from . models import *
# Register your models here.


class ProductImagesAdmin(admin.StackedInline):
    model = ProductImages

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'price', 'modified_date', 'is_available')
    inlines = [ProductImagesAdmin]


@admin.register(Variation)
class VariationsAdmin(admin.ModelAdmin):
    list_display = ['product' ,'color', 'stock']
    model = Variation



admin.site.register(ProductImages)
admin.site.register(Color)
admin.site.register(ReviewRating)

