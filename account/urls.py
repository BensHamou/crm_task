from django.urls import path
from .views import *


urlpatterns = [

    path('login_success/', login_success, name='login_success'),

    path("home/", homeView, name="home"),

    path("user/active/", listUserView, name="users"),
    path("user/refresh/", refreshUserList, name="refresh_users"),
    path("user/edit/<int:id>", editUserView, name="edit_user"),
    path("user/delete/<int:id>", deleteUserView, name="delete_user"),
    
    path('login/', CustomLoginView.as_view(), name='login'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logoutView, name='logout'),

]