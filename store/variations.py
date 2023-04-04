from django.shortcuts import render, redirect 
from django.contrib import messages
from . models import Product, Variation, Color
from admin_home.views import superadmin_check
from django.contrib.auth.decorators import user_passes_test



# ---------------- Variations -----------------


@user_passes_test(superadmin_check)
def variations(request):
    context = {
        'variations': Variation.objects.all().order_by('id'),
        'products': Product.objects.all().order_by('id'),
        'color': Color.objects.all().order_by('id'),
        
    }
    return render(request, 'adminhome/variation_management.html', context)


@user_passes_test(superadmin_check)
def add_variation(request):
    if request.method == 'POST':
        pro_name = request.POST['product']
        pro_color = request.POST['color']
        stock = int(request.POST['stock'])

        try:
            product = Product.objects.get(product_name=pro_name)
            color = Color.objects.get(color=pro_color)
            
        except:
            messages.warning(request, 'Oops!Something gone wrong.')
            return redirect(variations)

        if stock < 0:
            messages.error(request, 'Enter a valid stock')
            return redirect(variations)

        elif Variation.objects.filter(product=product, color=color).exists():
            messages.warning(
                request, f'Variation for {product} already exists')
            return redirect(variations)

        Variation.objects.create(
            product=product, color=color, stock=stock)
        messages.success(request, f'Variation addedd for the {product} succesfully')
        return redirect(variations)


@user_passes_test(superadmin_check)
def edit_variation(request, id):
    try:
        variation = Variation.objects.get(id=id)
    except Variation.DoesNotExist:
        messages.warning(request, 'Variation doesnot exist')
        return redirect(variations)

    if request.method == 'POST':
        pro_name = request.POST['product']
        pro_color = request.POST['color']
        
        stock = int(request.POST['stock'])
        

        try:
            product = Product.objects.get(product_name=pro_name)
            color = Color.objects.get(color=pro_color)
            
        except:
            messages.warning(request, 'Oops!Something gone wrong.')
            return redirect(variations)

        if stock < 0:
            messages.error(request, 'Enter a valid stock')
            return redirect(variations)

        elif Variation.objects.filter(product=product, color=color).exclude(id=id).exists():
            messages.warning(request, f'Variation for {product} already exists')
            return redirect(variations)

        else:
            variation.product = product
            variation.color = color
            variation.stock = stock
            variation.save()
            messages.success(
                request, f'Variation updated for the {product} succesfully')
            return redirect(variations)


@user_passes_test(superadmin_check)
def remove_variation(request, id):
    try:
        variation = Variation.objects.get(id=id)
        variation.delete()
        messages.success(request, 'Variation deleted successfully')
        return redirect(variations)
    except Variation.DoesNotExist:
        messages.warning(request, 'Oops!Something went wrong.')
        return redirect(variations)

# -----------------------------------------------------



#----------color management admin side -------------------

@user_passes_test(superadmin_check)
def add_color(request):
    if request.method == 'POST':
        color = request.POST['color']
        
        if Color.objects.filter(color=color).exists():
            messages.warning(request, 'color already exists')
            return redirect(variations)
        
        Color.objects.create(color=color)
        messages.success(request, 'color addedd succesfully')
        return redirect(variations)


@user_passes_test(superadmin_check)
def edit_color(request,id):
    if request.method == 'POST':

        try:
            color = Color.objects.get(id=id)
        except Color.DoesNotExist:

            messages.warning(request, 'Oops!Something gone wrong')
            return redirect(variations)
        
        edited_color =request.POST['color']
        color.color = edited_color
        color.save()
        messages.success(request, 'Color updated succesfully')
        return redirect(variations)
    

@user_passes_test(superadmin_check)
def remove_color(request,id):
    try:
        color = Color.objects.get(id=id)
        color.delete()
        messages.success(request, 'Color deleted succesfully')
        return redirect(variations)
    except Color.DoesNotExist:
        messages.error(request, 'Oops!Something gone wrong')
        return redirect(variations)