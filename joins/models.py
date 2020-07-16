from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django import forms

# Create your models here.


def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


class UserProfile(models.Model):
    tracker = models.ForeignKey(User, on_delete=models.CASCADE, default='1')
    rootid = models.IntegerField()
    title = models.CharField(max_length=10, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=25, default='', null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)

    user = models.IntegerField(default=1, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return 'UserProfile {}'.format(self.id)


class t_acct(models.Model):
    ACCOUNT_TYPE = (
        ('Attendant', 'Attendant'),
        ('Client', 'Client'),
        ('Staff', 'Staff'),
    )
    STATUS = (
        ('Active', 'Active'),
        ('NoneActive', 'NoneActive'),
    )
    GENDER = (
        ('Female', 'Female'),
        ('Male', 'Male'),
    )
    rootid = models.IntegerField(default=1000, null=True, blank=True)
    gender = models.CharField(
        choices=GENDER, max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=25, default='', null=True, blank=True)
    address = models.CharField(
        max_length=100, default='', null=True, blank=True)
    emergency_contact = models.CharField(max_length=100, null=True, blank=True)
    account_type = models.CharField(
        choices=ACCOUNT_TYPE, max_length=40, null=True, blank=True)
    status = models.CharField(
        choices=STATUS, max_length=20, null=True, blank=True)
    user = models.IntegerField(default=1, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('acct-delete', kwargs={'id': self.id})

    def __unicode__(self):
        return 't_acct {}'.format(self.id)
