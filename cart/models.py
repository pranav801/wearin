from django.db import models
from store.models import Product, Variation
from accounts.models import Account




#-------coupon---------------


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=20)
    discount_price = models.PositiveIntegerField(default=799)
    min_amount = models.PositiveIntegerField(default=17999)
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return self.coupon_code


#-------cart---------------


class Cart(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    cart_id = models.CharField(max_length=250, blank=True,null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    date_added = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    razorpay_order_id = models.CharField(max_length=100 ,null=True, blank=True,unique=True)

    def __str__(self):
        return self.user.email
    
    def get_cart_sub_total(self):
        cart_items = CartItem.objects.filter(cart=self.id)
        money = []
        for cart_item in cart_items:
            quantity = cart_item.quantity
            money.append(cart_item.product.price * quantity)

        return sum(money)

    def get_cart_total(self):
        cart_items = CartItem.objects.filter(cart=self.id)
        price = []
        for cart_item in cart_items:
            quantity = cart_item.quantity
            price.append(cart_item.product.price * quantity)


        if self.coupon:
            if self.coupon.min_amount < sum(price):
                return sum(price) - self.coupon.discount_price
            
        return sum(price)

    # Tax of cart_total
    def get_tax(self):
        return round(0.025 * self.get_cart_total(), 2)

    # tax + cart_total
    def get_grand_total(self):
        return self.get_cart_total() + self.get_tax()


class CartItem(models.Model): 
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    variant = models.ForeignKey(Variation, on_delete=models.SET_NULL, null=True, blank=True)

    

    def __str__(self):
        return str(Product.objects.get(id=self.product.id))
    
    # Product price
    def get_product_price(self):
        product_price = [self.product.price]

        return sum(product_price)

    # Cart item price
    def get_sub_total(self):
        price = [self.product.price]
        sub_total = sum(price) * self.quantity
        return sub_total
    

