from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product,Color
from cart.models import *
from order.models import PaymentMethod
from user_home.models import User_Address
from django.http import HttpResponse,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from .coupon import *
import razorpay

# Create your views here.


@login_required(login_url = 'login')
def cart(request,total=0, quantity=0, tax=0, grand_total=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user, is_active=True) 
            cart_items = CartItem.objects.filter(cart=cart)
       
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = round((2.8 * total)/100)
        grand_total = total + tax
        
    except ObjectDoesNotExist:
        pass #just ignore
    
    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total' : grand_total,
    }
    return render(request, 'userhome/cart.html', context)


@login_required(login_url = 'login')
def add_cart(request,product_id):
    variant=None
    current_user = request.user
    try:
        product = Product.objects.get(id=product_id) # get the product

        cart, _ = Cart.objects.get_or_create(user=current_user, is_active=True )
        

        if request.GET.get('variant'):
            variation = request.GET.get('variant')
            color = Color.objects.get(color=variation)
            variant = Variation.objects.get(product=product, color=color)
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart,variant=variant).exists()
        if is_cart_item_exists:
                cart_item = CartItem.objects.get(product=product, cart=cart)
                if cart_item.quantity == variant.stock:
                    messages.error(request, f'Only {cart_item.quantity} product in stock')
                    return redirect('cart')
                cart_item.variant = variant
                cart_item.quantity += 1
        else:
            cart_item = CartItem.objects.create(
                product=product,
                cart = cart,
                variant=variant,
                quantity = 1
            )
        cart_item.save()
        

    except:
        pass
    return redirect('cart')




@login_required(login_url = 'login')
def remove_cart(request, product_id, cart_item_id):

    try:
        product = Product.objects.get(id=product_id)
        cart = Cart.objects.get(user=request.user, is_active=True)
        cart_item = CartItem.objects.get(
            product=product, id=cart_item_id, cart=cart)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect('cart')


# Deleting item from the cart
@login_required(login_url = 'login')
def remove_cart_item(request,product_id,cart_item_id):   
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(user=request.user, is_active=True) 
    cart_item = CartItem.objects.filter(product=product, id=cart_item_id, cart=cart)
    cart_item.delete()
    return redirect('cart')




@login_required(login_url = 'login')
def checkout(request, total=0,quantity=0,cart_items=None):
    addresses = User_Address.objects.filter(user=request.user)
    name=User_Address.objects.filter()
    coupons = Coupon.objects.all()
    payment_method = PaymentMethod.objects.all()
    current_user = request.user
    global context   
    try:
        cart = Cart.objects.get(user=current_user, is_active=True)
        cart_items = CartItem.objects.filter(cart=cart)
        
        for item in cart_items:
            if item.quantity > item.variant.stock:
                item.quantity = item.variant.stock
                item.save()
                messages.warning(request, f'{item.product.product_name} has only {item.variant.stock} quantity left')
                return redirect('cart')
             
            
    except ObjectDoesNotExist:
        return redirect('cart')

    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains = coupon)

        if not coupon_obj.exists():
            messages.warning(request, 'Invalid coupon')
            return redirect(checkout)

        if cart.coupon:
            messages.warning(request, 'Coupon already exists')
            return redirect(checkout)


        if cart.get_cart_total() < coupon_obj[0].min_amount:
            messages.warning(request, f"Amount should be greater than {coupon_obj[0].min_amount}")
            return redirect(checkout)
                    
        if coupon_obj[0].is_expired:
            messages.warning(request, 'Coupon had been expired')
            return redirect(checkout)                


        cart.coupon = coupon_obj[0]#both if statement ontop fails then coupon_obj will get stored in cart_item.coupan,[0]?
        cart.save()  
        messages.success(request,'Coupon applied')
        return redirect(checkout)

    try:
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment = client.order.create({'amount': int(cart.get_grand_total()) * 100, 'currency': 'INR', 'payment_capture': 1})
        cart.razorpay_order_id=payment['id']
        cart.save()
    except:
        return redirect('cart')
    context = {
        'quantity':quantity,
        'cart_items':cart_items,
        'user_addresses': addresses,
        'name': name,
        'payment':payment,
        'cart' : cart,
        'coupons' : coupons,
        'method' : payment_method
    }
  

    return render(request, 'userhome/checkout.html',context)  

@login_required(login_url = 'login')
def remove_coupon(request):
    try:
        cart = Cart.objects.get(user=request.user, is_active=True)
        cart.coupon = None
        cart.save()
        messages.success(request, 'Coupon removed successfully')
    except:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))























