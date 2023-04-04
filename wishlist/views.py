from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product
from .models import Wishlist,WishlistItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url = 'login')
def _wishlist_id(request):
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    return wishlist

@login_required(login_url = 'login')
def add_wishlist(request,product_id):
    product = Product.objects.get(id=product_id)
    user = request.user

    # If user is authenticated
    if user.is_authenticated:
        try:
            wishlist_item = WishlistItem.objects.get(product=product, user=user)
            
        except WishlistItem.DoesNotExist:
            wishlist_item = WishlistItem.objects.create(
                product=product,
                user=user
            )
            wishlist_item.save()

    # If user is not authenticated
    
    else:
        try:
            wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
        except Wishlist.DoesNotExist: 
            wishlist = Wishlist.objects.create( 
                wishlist_id=_wishlist_id(request)
            )
        wishlist.save()  

        try:
            wishlist_item = WishlistItem.objects.get(product=product,wishlist=wishlist)
            wishlist_item.save()
        except WishlistItem.DoesNotExist:
            wishlist_item = WishlistItem.objects.create(
                product=product,
                wishlist=wishlist
            )
            wishlist_item.save()
    return redirect('wishlist')

@login_required(login_url = 'login')
def remove_wishlistitem(request,product_id):
    product = get_object_or_404(Product,id=product_id)
    user = request.user

    if user.is_authenticated:
        wishlist_item = WishlistItem.objects.get(product=product,user=user)
        wishlist_item.delete()
    
    return redirect('wishlist')





@login_required(login_url = 'login')
def wishlist(request,wishlist_items=None):
    user = request.user

    # If user is authenticated
    if user.is_authenticated:
        try:
            wishlist_items = WishlistItem.objects.filter(user=user,is_active=True)
            
        except WishlistItem.DoesNotExist:
            pass
        

    else:
        try:
            wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
            wishlist_items = WishlistItem.objects.filter(wishlist=wishlist,is_active=True)
            
        except ObjectDoesNotExist:
            pass

    context = {        
        'wishlist_items':wishlist_items,
    }
    
    return render(request, 'userhome/wishlist.html',context)