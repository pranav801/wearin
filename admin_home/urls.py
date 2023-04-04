from django.urls import path
from.import views


urlpatterns = [
    path('login/',views.admin_login,name='admin_login'),
    path('',views.dashboard,name='dashboard'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('usermanagement/',views.user_management,name='user_management'),
    path('user_action/<int:user_id>',views.user_action,name='user_action'),
    path('admin_profile/',views.admin_profile, name='admin_profile'), 
    path('admin_password/<int:user_id>',views.change_admin_password, name='change_admin_password'), 
    path('admin_profile_edit',views.admin_profile_edit, name='admin_profile_edit'), 
    path('admin_change_dp',views.admin_change_dp  ,name='admin_change_dp'),
]

