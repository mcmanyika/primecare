
from django.conf.urls import include, url
from django.contrib import admin
from joins.views import *
# from libs.views import *

urlpatterns = [
    url(r'^user-profile/', Userprofile, name='user-profile'),
    url(r'^register-member/$', register, name='register-member'),
    url(r'pending/', pending, name='pending'),
    url(r'^logout/$', Logout, name='logout'),
    url(r'^password/$', change_password, name='change_password'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^signup-confirmation/$', signup_confirmation, name='signup-confirmation'),


    url(r'^client/', client, name='client'),
    url(r'^client-detail/(?P<id>.*)$', client_detail, name='client-detail'),
    url(r'^staff/', staff, name='staff'),
    url(r'^staff-detail/(?P<id>.*)$', staff_detail, name='staff-detail'),
    url(r'^$', register_view, name='login'),

]
