from django.shortcuts import render,redirect,get_object_or_404
from .models import Advertisement
from django.contrib import messages
from admin_home.views import superadmin_check
from django.contrib.auth.decorators import user_passes_test

  
@user_passes_test(superadmin_check)
def ad_management(request):
    dict_ads={
        'adss': Advertisement.objects.all()
    }
    return render(request, 'adminhome/ads_management.html', dict_ads)

@user_passes_test(superadmin_check)
def delete_ads(request,ads_id):
    del_record = Advertisement.objects.filter(id=ads_id)
    del_record.delete()
    return redirect(ad_management)

@user_passes_test(superadmin_check)
def update_ads(request,ads_id):
    if request.method == 'POST':
        ad_name=request.POST['name']
        ad_des=request.POST['description'] 
        
        try:
            update_ads = Advertisement.objects.get(id=ads_id)
            image=request.FILES['image']
            update_ads.ad_image=image
            update_ads.save()
            messages.info(request,"Advertisment image updated successfully")
        except:
            pass

        if Advertisement.objects.filter(ad_name=ad_name).exists():
            messages.info(request,"This advertisment already exists")
            return redirect(ad_management)
        else:
            update_ads = Advertisement.objects.filter(id=ads_id)       
            update_ads.update(ad_name=ad_name,ad_description=ad_des)
            messages.info(request,"Advertisment updated successfully")
            return redirect(ad_management)

    else:
        messages.info(request,'some field is empty')
        return render(request,'adminhome/ads_managment.html')


@user_passes_test(superadmin_check)
def add_ads(request):
    try:
        if request.method == 'POST':
            ad_name=request.POST['name']
            ad_des=request.POST['description']   
            ad_image=request.FILES['image']
            if Advertisement.objects.filter(ad_name=ad_name).exists():
                messages.info(request,"This Advertisement already exists")
                return redirect(ad_management)
            else:
                ads = Advertisement.objects.create(ad_name=ad_name,ad_image=ad_image,ad_description=ad_des)
                ads.save()   
                messages.info(request,"Advertisement added successfully")        
            return redirect(ad_management)   
    except:
        messages.info(request,'some field is empty')
        return redirect(ad_management)