from django.urls import path
from accounts import views
from accounts.views import *

urlpatterns = [
    path('', views.index, name="index"),
    path('u_reg/',views.user_register,name='u_reg'),
    path('u_login/',views.users_login,name='user_login'),
    path('check_mail/', views.check_email, name="check_email"),
    path('u_logout/',views.user_logout,name='user_logout'),
    # path('change_pass/',views.change_password,name='change_password'),

#     # path('u_reg/',UserCreate.as_view(), name='u_reg'),


]