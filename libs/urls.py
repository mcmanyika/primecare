from django.contrib import admin
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from libs.views import *
from client.views import *

urlpatterns = [

    # url(r'^user-profile/', Userprofile, name='user-profile'),

    url(r'^add-staff/', add_staff, name='add-staff'),
    # url(r'^staff/', staff, name='staff'),
    # url(r'^staff-detail/(?P<id>.*)$', staff_detail, name='staff-detail'),

    url(r'^client/', client, name='client'),

    url(r'^libs/client-detail/(?P<id>.*)$',
        client_detail, name='client-detail'),
    url(r'^batch-detail/(?P<id>.*)$', batch_detail, name='batch-detail'),
    url(r'^edit-batch-detail/(?P<id>.*)$',
        edit_batch_detail, name='edit-batch-detail'),

    url(r'^libs/client-attribute-detail/(?P<id>.*)$',
        client_attribute_detail, name='client-attribute-detail'),

    url(r'^acct-delete/(?P<id>.*)$', acct_delete, name='acct-delete'),




    url(r'^billing-tracker/', billing_tracker, name='billing-tracker'),
    url(r'^billing/', billing, name='billing'),

    url(r'^employee-signin/', employee_signin, name='employee-signin'),
    url(r'^employee-signout/', employee_signout, name='employee-signout'),
    url(r'^add-client/', add_client, name='add-client'),

    url(r'^resources/', resources, name='resources'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
