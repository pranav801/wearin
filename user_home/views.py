from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from store.models import Category, Product
from advertisement.models import Advertisement
from .models import User_Address
from .forms import AddressForm
from accounts.models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
# Create your views here.



def home(request):
    dict_category = {
        'categories':Category.objects.all(),
        'product':Product.objects.all(),
        'ads': Advertisement.objects.all()

    }
    return render(request,'userhome/index.html', dict_category)

@login_required(login_url = 'login')
def user_profile(request):
    context = {
        'address':User_Address.objects.filter(user=request.user),
    }    
    return render(request,'userhome/user_profile.html', context)

def edit_address(request, address_id):
    address =User_Address.objects.get(id=address_id)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect(user_profile)
    else:
        form = AddressForm(instance=address)
    
    return render(request, 'userhome/edit-user-profile.html', {'form': form})

@login_required(login_url = 'login')
def add_address(request, num=0):
    address = User_Address.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = AddressForm(request.POST)
        
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()

            number = int(request.GET.get('num'))

            if number == 1:
                return redirect(user_profile)
            elif number == 2:
                return redirect('checkout')
        
        # if form is not valid, add an error message
        else:
            messages.error(request, 'Please correct the errors below.')
    
    else:
        form = AddressForm()
        
    return render(request,'userhome/add-user-profile.html',{'form':form, 'num':num})

@login_required(login_url = 'login')
def delete_address(request,address_id):
    User_Address.objects.get(id=address_id).delete()
    return redirect(user_profile)


@login_required(login_url = 'login')       
def default_address(request,id,num):
    User_Address.objects.filter(user=request.user,default=True).update(default=False)
    User_Address.objects.filter(pk=id,user=request.user).update(default=True)
    
    if num == 1:
         return redirect('user_profile')
    elif num == 2:
         return redirect('checkout')

@login_required(login_url = 'login')
def change_dp(request):
    user_id = request.user.id
    user = Account.objects.get(id=user_id)

    try:
        image = request.FILES['user_image']
        user.user_image=image
        user.save()
    except:
        pass
       
    return redirect(user_profile)



@login_required(login_url = 'login')
def password_edit(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']
        user = Account.objects.get(id=request.user.id)
        if not user.check_password(old_password):
            messages.error(request, 'Incorrect password')
            return redirect(user_profile)
        else:
            if new_password == confirm_new_password:
                user.set_password(new_password)
                user.save()
                auth.login(request,user)
                messages.success(request, 'Password changed succesfully!')
                return redirect(user_profile)
            else:
                messages.error(request, 'Password doesnot match.')
                return redirect(user_profile)
            
    return render(request,'userhome/user_profile.html')

@login_required(login_url = 'login')
def profile_edit(request):
    user_id = request.user.id

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        mobile =request.POST['phone']

        update_profile = Account.objects.filter(id=user_id)          
        update_profile.update(name=name, email=email,phone_number=mobile)
        messages.success(request, 'updated successfully !!')
        return redirect(user_profile)

    return render(request, 'userhome/user_profile.html') 

