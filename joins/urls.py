
from django.conf.urls import include, url
from django.contrib import admin
from joins.views import *
from libs.views import *

urlpatterns = [
    url(r'^user-profile/', Userprofile, name='user-profile'),
    url(r'^register-member/$', register, name='register-member'),
    url(r'pending/', pending, name='pending'),
    url(r'^logout/$', Logout, name='logout'),
    url(r'^password/$', change_password, name='change_password'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^signup-confirmation/$', signup_confirmation, name='signup-confirmation'),
    url(r'^user-img/$', user_img, name='user-img'),

    url(r'^staff-dashboard/', staff_dashboard, name='staff-dashboard'),


    url(r'^$', register_view, name='login'),

]
