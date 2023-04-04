from django.urls import path
from . import views


urlpatterns = [
    path('success/', views.place_order, name="success"),
    path('orderlist/', views.orders_list, name="orders_list"),
    path('order_details/<str:order_id>/', views.order_details, name="order_details"),
    path('order-tracking/<int:item_id>/', views.order_tracking, name="tracking"),
    path('order-invoice/<str:order_id>/', views.order_invoice, name="order_invoice"),
    path('cancel-order/<int:item_id>/<str:order_id>', views.cancel_order, name="cancel_order"),
    #admin
    path('orders_management/', views.orders_management, name="orders_management"),
    path('order_items/<int:id>/', views.order_items, name="order_items"),
    path('status-update/<int:id>/', views.status_update,name="status_update"),
]

