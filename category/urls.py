from django.contrib import admin
from django.urls import path
from category import views


urlpatterns = [
    path('', views.category_management, name='category_management'),    
    path('delete_category/<int:cate_id>', views.delete_category, name='delete_category'),
    path('update_category/<int:cate_id>/', views.update_category, name='update_category'),
    path('add_category', views.add_category, name='add_category'),
    path('brand/', views.brand_management, name='brand_management'),    
    path('delete_brand/<int:brand_id>', views.delete_brand, name='delete_brand'),
    path('update_brand/<int:brand_id>/', views.update_brand, name='update_brand'),
    path('add_brand', views.add_brand, name='add_brand'),
        
]
