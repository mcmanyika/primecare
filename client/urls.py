from django.contrib import admin
from django.conf.urls import include, url
from client.views import *

urlpatterns = [
    url(r'employee-dash/', employee_dash, name='employee-dash'),
    url(r'daily-logs/', daily_logs, name='daily-logs'),
    url(r'all-claims/', claims, name='all-claims'),
    url(r'^edit-billing-tracker/(?P<id>.*)$', edit_billing_tracker, name='edit-billing-tracker'),
    url(r'^delete-billing/(?P<id>.*)$', billing_delete, name='delete-billing'),
    
]