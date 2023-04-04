from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.ad_management, name='ad_management'),    
    path('add_ads', views.add_ads, name='add_ads'),
    path('update_ads/<int:ads_id>/', views.update_ads, name='update_ads'),
    path('delete_ads/<int:ads_id>', views.delete_ads, name='delete_ads'),
        
]

