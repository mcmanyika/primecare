from django.contrib import admin
from django.conf.urls import include, url
from frontend.views import *

urlpatterns = [
    url(r'^', site_index, name='site-index'),
    
]