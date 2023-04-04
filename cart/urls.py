from django.urls import path
from . import views


urlpatterns = [
    path('',views.cart,name="cart"),
    path('add_cart/<int:product_id>/',views.add_cart,name="add_cart"),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/',views.remove_cart,name="remove_cart"),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/',views.remove_cart_item,name="remove_cart_item"),
    path('checkout',views.checkout, name="checkout"),
    path('remove_coupon/', views.remove_coupon, name='remove_coupon'),
    

    #coupon
    path('coupon/', views.coupons, name="coupons"),
    path('add-coupon/', views.add_coupon, name="add_coupon"),
    path('edit-coupon/<int:id>/', views.edit_coupon, name="edit_coupon"),
    path('remove-coupon/<int:id>/', views.remove_coupon, name="remove_coupon"),
    path('coupon-status/<int:id>/', views.coupon_status, name="coupon_status"),

]
