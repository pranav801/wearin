from django.shortcuts import render, redirect
from cart.models import Coupon
from django.contrib import messages
from admin_home.views import superadmin_check
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(superadmin_check)
def coupons(request):
    context = {'coupons' : Coupon.objects.all()}
    return render(request, 'adminhome/coupon_management.html', context)


@user_passes_test(superadmin_check)
def add_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST['coupon_code']
        dis_price = int(request.POST['dis_price'])
        min_amount = int(request.POST['min_amount'])

        if Coupon.objects.filter(coupon_code__iexact=coupon_code).exists():
            messages.warning(request, 'Coupon already exists')
            return redirect(coupons)
        
        elif dis_price > min_amount :
            messages.warning(request, 'Discount price should be less than minimum amount')
            return redirect(coupons)
        
        elif (dis_price or min_amount) <= 0 :
            messages.warning(request, 'Enter a valid discount price/minimum amount')
            return redirect(coupons)
        
        coupon = Coupon.objects.create(coupon_code=coupon_code, discount_price=dis_price, min_amount=min_amount)
        coupon.save()
        messages.success(request, f'Coupon {coupon_code} addedd succesfully')
        return redirect(coupons)
    

@user_passes_test(superadmin_check)
def edit_coupon(request, id):
    if request.method == 'POST':
        coupon_code = request.POST['coupon_code']
        dis_price = int(request.POST['dis_price'])
        min_amount = int(request.POST['min_amount'])

        try:
            coupon = Coupon.objects.get(id=id)
        except Coupon.DoesNotExist:
            messages.warning(request, 'Oops!Something went wrong')
            return redirect(coupons)
        
        if Coupon.objects.filter(coupon_code__iexact=coupon_code).exclude(id=id).exists():
            messages.warning(request, 'Coupon already exists')
            return redirect(coupons)
        
        elif dis_price > min_amount :
            messages.warning(request, 'Discount price should be less than minimum amount')
            return redirect(coupons)
        
        elif (dis_price or min_amount) <= 0 :
            messages.warning(request, 'Enter a valid discount price/minimum amount')
            return redirect(coupons)
        
        
        coupon.coupon_code = coupon_code
        coupon.discount_price = dis_price
        coupon.min_amount = min_amount
        coupon.save()
        messages.success(request, 'Coupon updated succesfully')
        return redirect(coupons)


@user_passes_test(superadmin_check)
def remove_coupon(request, id):
    try:
        coupon = Coupon.objects.get(id=id)
        coupon.delete()
        messages.success(request, 'Coupon deleted succesfully')
        return redirect(coupons)
    except Coupon.DoesNotExist:
        messages.warning(request, 'Oops!Something gone wrong')
        return redirect(coupons)


@user_passes_test(superadmin_check)
def coupon_status(request, id):
    try:
        coupon = Coupon.objects.get(id=id)

        if coupon.is_expired:
            coupon.is_expired = False
            coupon.save()
            messages.success(request, f'Coupon {coupon} activated succesfully')
            return redirect(coupons)
        
        else:
            coupon.is_expired = True
            coupon.save()
            messages.success(request, f'Coupon {coupon} deactivated succesfully')
            return redirect(coupons)
        
    except Coupon.DoesNotExist:
        messages.error(request, 'Oops!Something gone wrong')
        return redirect(coupons)