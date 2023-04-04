from django.shortcuts import render, redirect ,get_object_or_404
from . models import Product, ProductImages, Variation, ReviewRating
from category.models import Category, Brand
from category import models as category
from django.contrib import messages
from django.core.paginator import Paginator
from wishlist.models import WishlistItem
from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from .review import *
from .variations import *
from django.db.models import Count
from admin_home.views import superadmin_check
from django.contrib.auth.decorators import user_passes_test

# Products view
def shop(request,category_slug=None,brand_slug=None):
    categories = None
    products = None

   

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products =Product.objects.filter(category=categories,is_available=True) 
        products_count = products.count()

    elif brand_slug != None:
        brands = get_object_or_404(Brand, slug=brand_slug)
        print(brands)
        products = Product.objects.filter(brand=brands,is_available=True)    
        products_count = products.count
    
    elif request.GET.get('min'):
        min = request.GET.get('min')
        max = request.GET.get('max')
        products = Product.objects.filter(price__range=(min, max))
        products_count = products.count

    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')   
        products_count = products.count()

    sort_by = request.GET.get('sort_by')
    if sort_by == 'name_a_to_z':
        products = products.order_by('product_name')

    elif sort_by == 'name_z_to_a':
        products = products.order_by('-product_name')

    elif sort_by == 'price_low_to_high':
        products = products.order_by('price')

    elif sort_by == 'price_high_to_low':
        products = products.order_by('-price')

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    brand_ids = request.GET.getlist('brand')
    category_ids = request.GET.getlist('category')

    if brand_ids and category_ids:
        products = Product.objects.filter(brand__in=brand_ids, category__in=category_ids)

    elif brand_ids:
        products = Product.objects.filter(brand__in=brand_ids)

    elif category_ids:
        products = Product.objects.filter(category__in=category_ids)

    brands = category.Brand.objects.annotate(product_count=Count('product'))
    categories = category.Category.objects.annotate(product_count=Count('product'))

    context = {
        'products' : products, 
        'count' : products_count,
        'categories': categories,
        'brands': brands,
           
    }
    return render (request,'userhome/shop.html',context)


# Single product detail
def product_detail(request, category_slug, product_slug):
    in_wishlist = False
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        variants = Variation.objects.filter(product=single_product)
        context = {
            'single_product': single_product,
            'variants': variants,
            'images': ProductImages.objects.filter(product=single_product),
            'review': ReviewRating.objects.filter(product=single_product),
            'reviews': ReviewRating.objects.filter(product=single_product).count(),
            }

        if request.GET.get('variant'):
            
            color = request.GET.get('variant')

            context.update({
                'selected_variant': color,                             
            }) 

        if request.user.is_authenticated:
            # wishlist = Wishlist.objects.get()
            in_wishlist = WishlistItem.objects.filter(user=request.user, product__product_name=single_product)
            context['in_wishlist'] = in_wishlist

        return render(request, 'userhome/product-detail.html', context)

    except Exception as e:
        raise e

 
# Search
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(brand__brand_name__icontains=keyword) | Q(product_name__icontains=keyword))
            products_count = products.count()

    context = {
        'products' : products,
        'products_count' : products_count,
    }

    return render (request,'userhome/shop.html',context)




#product management by admin side

@user_passes_test(superadmin_check)
def product_management(request):
    categories = Category.objects.all()    
    products = Product.objects.all()
    brands = Brand.objects.all()
    return render(request, 'adminhome/product_management.html', {'products': products,'categories': categories, 'brands': brands})

@user_passes_test(superadmin_check)
def delete_product(request,product_id):
    del_record = Product.objects.filter(id=product_id)
    del_record.delete()
    return redirect(product_management)   

@user_passes_test(superadmin_check)
def update_product(request,product_id):
    products=get_object_or_404(Product,pk=product_id)
    categories = Category.objects.all()    
    if request.method == 'POST':
        try:
            update_prod=Product.objects.get(id=product_id)
            product_image=request.FILES['image']
            update_prod.images=product_image
            update_prod.save()
        except:
            pass

        product=request.POST['product']
        category=request.POST['category']
        brand=request.POST['brand']
        product_des=request.POST['description']
        price=request.POST['price']
        brand_instance = Brand.objects.get(brand_name=brand)
        cat_instance = Category.objects.get(cat_name=category)
         
        update_prod=Product.objects.filter(id=product_id)
        update_prod.update(product_name=product,description=product_des,category=cat_instance,brand=brand_instance,price=price)
        context = {'product': products, 'categories': categories}
        return redirect(product_management)

    else:    
        messages.info(request,'some field is empty')
        return render(request,'adminhome/product_management.html', context)


@user_passes_test(superadmin_check)
def add_product(request):
    if request.method == 'POST':
        price=request.POST['price']
        productname=request.POST['product']

        product_des=request.POST['description']
        category=request.POST['category']
        brand=request.POST['brand']
        multi_image = request.FILES.getlist('imagess')

        brand_instance = Brand.objects.get(id=brand)
        cat_instance = Category.objects.get(id=category)
        try:
            product_image = request.FILES['image']
        except MultiValueDictKeyError:
            messages.info(request, 'image is not uploaded')
            return redirect(product_management)        
        # null value checking 
        check = [price]
        for values in check:
            if values == '':
                messages.error(request,'some fields are empty')
                return redirect(product_management)
            else:
                pass

        # checking price and quantity is number
        try:
            check_number = int(price)
            
        except:
            messages.danger(request,'number field got unexpected values')
            return redirect(product_management)

        # checking price and quantity positive number
        try:
            check_pos = [int(price)]
        except ValueError:
            messages.danger(request, 'Price and stock must be valid integers')
            return redirect(product_management)

        for value in check_pos:
            if value < 0:
                messages.info(request, 'Price and stock should be positive numbers')
                return redirect(product_management)

        prod = Product.objects.create(product_name=productname,images=product_image,description=product_des,category=cat_instance,price=price,brand=brand_instance)
        prod.save() 
        for image in multi_image:
            ProductImages.objects.create(
                product=prod, 
                imagess=image
                )            
        return redirect(product_management)
  
    else:
        return redirect(add_product)





