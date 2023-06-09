from .models import Cart,CartItem



def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        if request.user.is_authenticated:
            try:
                cart = Cart.objects.filter(user=request.user)
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            except Cart.DoesNotExist:
                cart_count=0

    return dict(cart_count=cart_count)
