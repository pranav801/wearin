from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop,name="allProducts"),
    path('search/',views.search,name="search"),
    path('category/<slug:category_slug>/', views.shop,name="products_by_category"),
    path('brand/<slug:brand_slug>/', views.shop,name="products_by_brand"),
    path('products/', views.shop,name="price_sorting"),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail,name="product_detail"),

    #product management
    path('product/', views.product_management, name="product_management"),   
    path('add_product', views.add_product, name='add_product'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),  
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),

    #review rating
    path('submit_review/<int:product_id>', views.submit_review, name='submit_review'),
    path('deletereview/<int:id>/', views.deleteReview, name='deletereview'),
    path('review-managemet/', views.review_management, name="review_management"),
    path('remove-review/<int:id>/', views.remove_review, name="remove_review"),

    # Variations
    path('variations/', views.variations, name='variations'),
    path('add-variation/', views.add_variation, name='add_variation'),
    path('edit-variation/<int:id>/', views.edit_variation, name='edit_variation'),
    path('remove-variation/<int:id>/', views.remove_variation, name='remove_variation'),

    #color
    path('add-color/',views.add_color,name="add_color"),
    path('edit-color/<int:id>/',views.edit_color, name="edit_color"),
    path('remove-color/<int:id>/',views.remove_color,name="remove_color"),

]