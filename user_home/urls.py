from django.urls import path
from.import views


urlpatterns = [
    path('',views.home,name='home'),
    path('profile/',views.user_profile,name='user_profile'),
    path('edit-address/<int:address_id>',views.edit_address,name='edit_address'),
    path('add-address/<int:num>/',views.add_address,name='add_address'),
    path('change_dp',views.change_dp  ,name='change_dp'),
    path('delete_address/<int:address_id>',views.delete_address  ,name='delete_address'),
    path('default_address/<int:id>/<int:num>/',views.default_address  ,name='default_address'),
    path('edit-profile',views.profile_edit  ,name='profile_edit'),
    path('edit-password/',views.password_edit  ,name='password_edit'),
]

