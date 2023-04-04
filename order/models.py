from django.db import models
from accounts.models import Account
from base.models import BaseModel
from user_home.models import User_Address
from store.models import Product, Variation
from cart.models import Coupon
# Create your models here.



class PaymentMethod(models.Model):
    method = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.method
    


class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100,null=True)
    cart_total = models.PositiveIntegerField()
    tax = models.PositiveIntegerField()
    grand_total = models.PositiveIntegerField()
    sub_total = models.PositiveBigIntegerField(null=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=True)
    paid_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username


class Order(BaseModel):
    order_id = models.CharField(max_length=100, unique=True)
    coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    delivery_address = models.ForeignKey(User_Address, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.id} of {self.user}'

class OrderItem(models.Model):
    STATUS = (
        ('Ordered', 'Ordered'),
        ('Shipped', 'Shipped'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Refunded', 'Refunded')
    )
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.CharField(max_length=100, null=True,blank=True)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE, null=True, blank=True)
    order_status = models.CharField(max_length=20, choices=STATUS, default='Ordered')
    item_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    item_total = models.PositiveIntegerField()


    def __str__(self):
        return self.product.product_name