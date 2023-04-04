from category.models import Category,Brand

def menu_links(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    return dict(categories=categories,brands=brands)