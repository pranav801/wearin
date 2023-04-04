from django.shortcuts import render, redirect
from django.contrib.auth.models import  User
from django.contrib import messages, auth
from django.shortcuts import get_object_or_404
from eCommerce import settings
from order.models import Order, OrderItem, Payment
from user_home.models import Account
from django.db.models import Sum
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.db.models import Sum, DateField

from datetime import datetime, timedelta
from django.db.models.functions import TruncDay, Cast



def superadmin_check(user):
    return user.is_superadmin



def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email,password=password)
        print(user)
        if user is not None:
            if user.is_admin:
                auth.login(request,user)
                return redirect(dashboard)
            else:
                messages.error(request,f"{user.name} is not have admin access")
                return redirect(admin_login)
        else:
            messages.info(request,'credential mismatch')
            return redirect(admin_login)
    else:
        return render(request,'adminhome/admin_login.html')


@user_passes_test(superadmin_check)
def dashboard(request):
    sales = OrderItem.objects.all().count()
    users = Account.objects.all().count()
    recent_sales = Order.objects.order_by('-id')[:5]
    total_income = Payment.objects.aggregate(Sum('grand_total'))['grand_total__sum'] 
    total_income = round(total_income, 2)

    # Graph setting
    # Getting the current date
    today = datetime.today()
    date_range = 8

    # Get the date 7 days ago
    four_days_ago = today - timedelta(days=date_range)

    #filter orders based on the date range
    payments = Payment.objects.filter(paid_date__gte=four_days_ago, paid_date__lte=today)

    # Getting the sales amount per day
    sales_by_day = payments.annotate(day=TruncDay('paid_date')).values('day').annotate(total_sales=Sum('grand_total')).order_by('day')

    # Getting the dates which sales happpened
    sales_dates = Payment.objects.annotate(sale_date=Cast('paid_date', output_field=DateField())).values('sale_date').distinct()
    

    context = {
        'sales' : sales,
        'users' : users,
        'revenue' : total_income,
        'sales_by_day' : sales_by_day,
        'sales_dates' :sales_dates,
        'recent_sales' :recent_sales,        
    }
    return render(request, 'adminhome/dashboard.html',context)

@user_passes_test(superadmin_check)
def admin_logout(request):
    auth.logout(request)
    return redirect(admin_login)


@user_passes_test(superadmin_check)
def user_management(request):
    dict_user = {
        'users':Account.objects.all().order_by('id')
    }
    return render(request,'adminhome/user_management.html',dict_user)

@user_passes_test(superadmin_check)
def user_action(request,user_id):
    user = Account.objects.get(id=user_id)
    
    if user.is_blocked:
        user.is_blocked=False
        user.save()
        mess=f'Hello\t{user.name},\n Your WeariN account is unblocked by admin\n Now you can surf in the world of WeariN premium watches' 
        send_mail(
                'Your account is unblocked by admin',
                mess,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )
        messages.success(request, 'User unblocked succesfully!')
        
        return redirect(user_management)
    else:
        user.is_blocked=True
        user.save()
        mess=f'Hello\t{user.name},\n Your WeariN account is blocked by admin'
        send_mail(
                'You account is blocked, contact admin for more details',
                mess,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )
        messages.success(request, 'User blocked succesfully!')
        return redirect(user_management)

@user_passes_test(superadmin_check)
def admin_profile(request):
    
    return render(request, 'adminhome/admin_profile.html')

@user_passes_test(superadmin_check)
def change_admin_password(request, user_id):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']
        user = Account.objects.get(id=user_id)
        if not user.check_password(old_password):
            messages.error(request, 'Incorrect password')
            return redirect(admin_profile)
        else:
            if new_password == confirm_new_password:
                user.set_password(new_password)
                user.save()
                auth.login(request,user)
                messages.success(request, 'Password changed succesfully!')
                return redirect(admin_profile)
            else:
                messages.error(request, 'Password doesnot match.')
                return redirect(admin_profile)
            
    return render(request,'adminhome/admin_profile.html')

@user_passes_test(superadmin_check)
def admin_change_dp(request):
    user_id = request.user.id
    user = Account.objects.get(id=user_id)

    try:
        image = request.FILES['user_image']
        user.user_image=image
        user.save()
    except:
        pass
       
    return redirect(admin_profile)

@user_passes_test(superadmin_check)
def admin_profile_edit(request):
    user_id = request.user.id

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']

        update_profile = Account.objects.filter(id=user_id)          
        update_profile.update(name=name, email=email)
        messages.success(request, 'updated successfully !!')
        return redirect(admin_profile)

    return render(request, 'adminhome/admin_profile.html') 



