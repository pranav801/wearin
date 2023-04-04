from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Category, Brand
from store.models import Product
from admin_home.views import superadmin_check
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(superadmin_check)
def category_management(request):
    dict_cate={
        'cate': Category.objects.all().order_by('id')
    }
    return render(request,'adminhome/category_managment.html',dict_cate)
    
@user_passes_test(superadmin_check)    
def delete_category(request,cate_id):
    del_record = Category.objects.filter(id=cate_id)
    del_record.delete()
    messages.info(request,"Category deleted successfully")
    return redirect(category_management)

@user_passes_test(superadmin_check)
def update_category(request,cate_id):
    products=get_object_or_404(Category,pk=cate_id)
    if request.method == 'POST':
        category=request.POST['category']
        
        try:
            update_category = Category.objects.get(id=cate_id)
            #this update_c was given to get the perticular id wala img so that we can save it
            image=request.FILES['image']
            update_category.cat_image=image
            update_category.save()
        except:
            pass

        if Category.objects.filter(cat_name=category).exists():
            messages.info(request,"This category already exists")
            return redirect(category_management)
        else:
            update_category = Category.objects.filter(id=cate_id)  
        # this update_c was given to filter all the id in the category        
            update_category.update(cat_name=category)
            messages.info(request,"Category updated successfully")
            return redirect(category_management)

        #here both the update_c were imp because both play 2 diff roles 
    else:
        messages.info(request,'some field is empty')
        return render(request,'adminhome/category_managment.html')


@user_passes_test(superadmin_check)
def add_category(request):
    if request.method == 'POST':
        category = request.POST['category']
        image=request.FILES['image']
          
        if Category.objects.filter(cat_name=category).exists():
            messages.info(request,"This category already exists")
            return redirect(category_management)
        else:
            cate = Category.objects.create(cat_name=category,cat_image=image)
            cate.save() 
            messages.info(request,"Category added successfully")          
        return redirect(category_management)   
  
    else:
        messages.info(request,'some field is empty')
        return redirect(add_category)
    



#Brand management
@user_passes_test(superadmin_check)
def brand_management(request):
    dict_brand={
        'brands': Brand.objects.all().order_by('id')
    }
    return render(request,'adminhome/brand_management.html',dict_brand)

@user_passes_test(superadmin_check)    
def delete_brand(request,brand_id):
    del_record = Brand.objects.filter(id=brand_id)
    del_record.delete()
    messages.info(request,"Brand deleted successfully")
    return redirect(brand_management)

@user_passes_test(superadmin_check)
def update_brand(request,brand_id):
    products=get_object_or_404(Brand,pk=brand_id)
    if request.method == 'POST':
        brand=request.POST['brand']
         

        if Brand.objects.filter(brand_name=brand).exists():
            messages.info(request,"This brand already exists")
            return redirect(brand_management)
        else:
            update_brand = Brand.objects.filter(id=brand_id)  
        # this update_c was given to filter all the id in the category        
            update_brand.update(brand_name=brand)
            messages.info(request,"Brand updated successfully")
            return redirect(brand_management)

        #here both the update_c were imp because both play 2 diff roles 
    else:
        messages.info(request,'some field is empty')
        return render(request,'adminhome/brand_management.html')


@user_passes_test(superadmin_check)
def add_brand(request):
    if request.method == 'POST':
        brand = request.POST['brand']
        
        if Brand.objects.filter(brand_name=brand).exists():
            messages.info(request,"This brand already exists")
            return redirect(brand_management)
        else:
            brand = Brand.objects.create(brand_name=brand)
            messages.info(request,"Brand added successfully")
            brand.save()           
        return redirect(brand_management)   
  
    else:
        messages.info(request,'some field is empty')
        return redirect(add_brand)