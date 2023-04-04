from django.contrib import admin
from .models import Category,Brand

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug' : ('cat_name',)}
    list_display = ('cat_name', 'slug')

class BrandAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('brand_name',)}
    list_display = ('brand_name', 'slug')

admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)