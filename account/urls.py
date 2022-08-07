from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth.views import LogoutView
from django.views.generic import RedirectView

from .views import *

urlpatterns = [
    path('signup/', signup_page_func, name='register'),
    path('login/', login_page_func, name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('users/create/', user_create_func, name='user_create'),
    path('users/login/', login_func, name='user_login'),
    path('users/update/', user_update_func, name='user_update'),

    path('profile/', RedirectView.as_view(url='/'), name='profileToCompany'),

    re_path(r'confirm/user/signup/(?P<slug>[-\w]+)/', confirm_user_create, name='confirm_user_create'),

    path('testconfirmemailtemplate', testconfirmemailtemplate, name='testconfirmemailtemplate'),

    path('reset_pass/', reset_password, name='reset_pass'),
    re_path(r'reset_pass/(?P<slug>[-\w]+)/', confirm_reset_password, name='confirm_reset_password')
]