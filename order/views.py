from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse
from user_home.models import User_Address
from cart.models import Cart, CartItem
from .models import *
from cart.models import Cart, CartItem
from .models import Payment,Order,OrderItem,PaymentMethod
from django.utils import timezone
from django.contrib import messages
import razorpay
from django.conf import settings
from admin_home.views import superadmin_check
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
import uuid
import eCommerce.settings
from django.contrib.auth.decorators import login_required


@login_required(login_url = 'login')
def place_order(request):
    razorpay_order_id =None
    payment_method = request.GET.get('method')
    method_instance = PaymentMethod.objects.get(id=int(payment_method))

    address_id = request.GET.get('addrs')
    delivery_address = User_Address.objects.get(id=address_id)

    try:
        razorpay_order_id = request.GET.get('razorpay_order_id')
        cart = Cart.objects.get(user=request.user, is_active=True)
    except:
        return redirect('cart')
    
    
    # Payment details storing
    user = request.user
    transaction_id = request.GET.get('razorpay_payment_id')
    cart_total = cart.get_cart_total()
    sub_total = cart.get_cart_sub_total()
    tax = cart.get_tax()
    grand_total = cart.get_grand_total()
    payment = Payment.objects.create(
        payment_method= method_instance,user=user, transaction_id=transaction_id, 
        cart_total=cart_total, tax=tax, grand_total=grand_total, sub_total=sub_total)
    payment.save()
    

    #Creating the order in Order table
    order_id = uuid.uuid4().hex[:10] # generate a random 10-character hex string
    order = Order.objects.create(order_id=order_id, user=user, delivery_address=delivery_address, payment=payment)

    if cart.coupon:
        order.coupon=cart.coupon
        order.save()


    # Storing ordered products in OrderItem table
    order_items = CartItem.objects.filter(cart=cart)
    for item in order_items:
        ordered_item = OrderItem.objects.create(user=user,order=order, product=item.product, item_price=item.get_product_price(), quantity=item.quantity, item_total=item.get_sub_total())
        ordered_item.save()
        if item.variant:
            item.variant.stock -= item.quantity
            item.variant.save()
           
            ordered_item.variation = item.variant
            ordered_item.save()
            
            current_user = request.user
            subject = "Order Successfull"
            mess = f'Dear {current_user.name}, \nWe are pleased to inform you that your order {item} with order number {order.order_id} has been successfully placed. Thank you for choosing to shop with us \nBest Regards \nWeariN'
            send_mail(
                        subject,
                        mess,
                        settings.EMAIL_HOST_USER,
                        [current_user.email],
                        fail_silently = False
                        )      

    #Deleting the cart once it is ordered/paid
    cart.is_active = False
    cart.delete()

    return render(request, 'userhome/thankyou.html', {'order_id': razorpay_order_id})


@login_required(login_url = 'login')
def orders_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'userhome/orders_list.html', {'orders' : orders})


@login_required(login_url = 'login')
def order_details(request,order_id):
    try:
        order = Order.objects.get(uid=order_id)
        order_items = OrderItem.objects.filter(order=order,user=request.user)
        
    except:
        order_items = None 
    return render(request, 'userhome/order_details.html', {'order_items' : order_items})


@login_required(login_url = 'login')
def order_tracking(request, item_id):
    current_date = timezone.now()
    item = OrderItem.objects.get(id=item_id)
    print(item.order.payment.payment_method)
    context = {
        'item' : item,
        'current_date' : current_date
    }
    return render(request, 'userhome/order_tracking.html' ,context)


@login_required(login_url = 'login')
def order_invoice(request, order_id):
    order = Order.objects.get(uid=order_id,user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    payment = Payment.objects.filter(order=order)
    context = {
        'payment':payment,
        'order' : order,
        'order_items' : order_items
    }
    return render(request, 'userhome/invoice.html',context)

@login_required(login_url = 'login')
def cancel_order(request, item_id=None, order_id=None):
        
    order = Order.objects.get(order_id=order_id,user=request.user)
    item = OrderItem.objects.get(order=order, id=item_id)
    
    if order.payment == 2:
        client = razorpay.Client(auth=(eCommerce.settings.API_KEY, eCommerce.settings.RAZORPAY_SECRET_KEY))
        payment_id = order.payment.transaction_id
        item_amount = item.order.payment.grand_total
        
        refund = client.payment.refund(payment_id,{'amount':item_amount})
       
        
        if refund is not None:
            item.order_status = 'Refunded'
            item.variation.stock += item.quantity
            item.variation.save()

            current_user = request.user
            subject = "Refund succesfull!"
            mess = f'Greetings {current_user.name},\nYour refund for the product {item} of order: {order.order_id} has been succesfully generated. \nThank you for shopping with us!\nWeariN'
            send_mail(
                        subject,
                        mess,
                        settings.EMAIL_HOST_USER,
                        [current_user.email],
                        fail_silently = False
                     )

            item.save()
            return render(request, 'userhome/cancel-order.html',{'order_id':order_id})

        else:
            return HttpResponse('Payment not captured')
    else:   
        item.order_status = 'Refunded'
        item.variation.stock += item.quantity
        item.variation.save()

        current_user = request.user
        subject = "Order Cancellation Confirmation "
        mess = f'Dear {current_user.name}, \nWe regret to inform you that your order "{item}" with order number {order.order_id}, which was placed on {order.ordered_date}, has been cancelled. We apologize for any inconvenience this may have caused.\nThank you \nWeariN'
        send_mail(
                    subject,
                    mess,
                    settings.EMAIL_HOST_USER,
                    [current_user.email],
                    fail_silently = False
                    )

        item.save()
        return render(request, 'userhome/cancel-order.html',{'order_id':order_id})

       
        
@user_passes_test(superadmin_check)
def orders_management(request):

    context = {
        'orders' : Order.objects.all().order_by('-id'),
        'order_items' : OrderItem.objects.all()
    }
    return render(request, 'adminhome/order_management.html', context)



@user_passes_test(superadmin_check)
def order_items(request, id):
    try:
        orders = Order.objects.get(id=id)
        order_items = OrderItem.objects.filter(order=orders).order_by('id')
        return render(request, 'adminhome/order-details-admin.html', {'order_items' : order_items})
    
    except:
        messages.error(request, 'Oops!Something gone wrong')
        return redirect(orders_management)
    


@user_passes_test(superadmin_check)
def status_update(request, id):
    try:
        order_item = OrderItem.objects.get(id=id)
        if request.method == 'POST':
            status = request.POST['status']
            order_item.order_status = status
            order_item.save()
            messages.success(request, 'Status updated successfully')
            mess=f'Hello\t{order_item.user.name},\n Your order {order_item.product.product_name} has been {order_item.order_status} successfully\n Track your order status in our website \n Thank you' 
            send_mail(
                    'Order status',
                    mess,
                    settings.EMAIL_HOST_USER,
                    [order_item.user.email],
                    fail_silently=False
                )
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    except OrderItem.DoesNotExist:
        messages.error(request, 'Oops!Something gone wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    



