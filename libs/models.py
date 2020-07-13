from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from multiselectfield import MultiSelectField
from django import forms
from joins.models import *

# Create your models here.


def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


class t_accts(models.Model):
    rootid = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, null=True, blank=True)
    dob = models.CharField(max_length=15, null=True, blank=True)
    phone = models.CharField(max_length=25, default='', null=True, blank=True)
    address = models.CharField(
        max_length=100, default='', null=True, blank=True)
    email = models.CharField(max_length=50, default='', null=True, blank=True)
    emergency_contact = models.CharField(max_length=100, null=True, blank=True)
    account_type = models.CharField(max_length=40, null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True)
    user = models.IntegerField(default=1, null=True, blank=True)

    def __unicode__(self):
        return 't_accts {}'.format(self.id)


class t_patient_acct(models.Model):

    fname = models.CharField(max_length=10, null=True, blank=True)
    lname = models.CharField(max_length=10, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=25, default='', null=True, blank=True)
    address = models.CharField(
        max_length=100, default='', null=True, blank=True)

    user = models.IntegerField(default=1, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return 't_patient_acct {}'.format(self.id)


class Client(models.Model):
    Daily_Login_ID = models.CharField(
        max_length=20, default='', null=True, blank=True)
    Daily_Logout_ID = models.CharField(
        max_length=20, default='', null=True, blank=True)
    PatientID = models.IntegerField(null=True, blank=True)
    employee_id = models.IntegerField(null=True, blank=True)
    user = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return 'Client {}'.format(self.id)


class t_dict(models.Model):
    header = models.CharField(max_length=50, default='')
    category = models.CharField(max_length=20, default='')
    status = models.CharField(max_length=20, default='')
    user = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return 't_dict {}'.format(self.id)


class t_visit_tracker(models.Model):
    rootid = models.ForeignKey(t_accts, on_delete=models.CASCADE, default='1')
    date = models.DateField()
    status = models.CharField(max_length=20, default='', null=True, blank=True)
    employee_id = models.IntegerField(null=True, blank=True)
    user = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return 't_visit_tracker {}'.format(self.id)


class t_oig(models.Model):
    rootid = models.ForeignKey(t_accts, on_delete=models.CASCADE)
    root = models.IntegerField(null=True, blank=True)
    site = models.CharField(max_length=100, default='')
    date = models.DateField()
    document = models.FileField(upload_to='documents/oig/')
    user = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return 't_oig {}'.format(self.id)


class t_url(models.Model):
    header = models.CharField(max_length=50, default='')
    category = models.CharField(max_length=20, default='')
    url = models.CharField(max_length=100, default='')
    icon = models.CharField(max_length=20, default='')
    toggle = models.CharField(max_length=20, default='collapse')
    order = models.IntegerField(default='1')
    status = models.CharField(max_length=20, default='')
    user = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return 't_url {}'.format(self.id)


class t_sub_url(models.Model):
    rootid = models.ForeignKey(t_url, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, default='', null=True, blank=True)
    url = models.CharField(max_length=100, default='', db_index=True)
    slug = models.SlugField(max_length=100, default='',
                            unique=True, db_index=True)
    toggle = models.CharField(max_length=20, default='modal')
    page_type = models.CharField(
        max_length=20, default='', null=True, blank=True)
    status = models.CharField(max_length=20, default='', null=True, blank=True)
    user = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return 't_sub_url {}'.format(self.id)

    def get_absolute_url(self):
        return reverse('dashboard:product_detail', args=[self.id, self.slug])


class t_resources(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=50, default='')
    category = models.CharField(max_length=100, default='')
    document = models.FileField(upload_to='documents/resources/')
    user = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return 't_resources {}'.format(self.id)


class t_sub_resources(models.Model):
    rootid = models.ForeignKey(t_resources, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=50, default='')
    category = models.CharField(max_length=100, default='')
    document = models.FileField(upload_to='documents/resources/')
    user = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return 't_sub_resources {}'.format(self.id)
