from __future__ import unicode_literals
from django.conf import settings
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse    
from django import forms           

# Create your models here.
def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)


class UserProfile(models.Model):
    tracker = models.ForeignKey(User, on_delete=models.CASCADE, default='1')
    rootid = models.IntegerField()
    title = models.CharField(max_length=10, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=25, default='', null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    image_thumbnail = ImageSpecField(source='avatar',
        processors=[ResizeToFill(350, 200)],
        format='JPEG',
        options={'quality': 60})

    user = models.IntegerField(default=1, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now=False)
    updated = models.DateTimeField(auto_now_add = False, auto_now=True)

    def __unicode__(self):
        return 'UserProfile {}'.format(self.id) 



class t_accts(models.Model):

    fname = models.CharField(max_length=20, null=True, blank=True)
    middle_name = models.CharField(max_length=20, null=True, blank=True)
    lname = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    dob = models.CharField(max_length=15, null=True, blank=True)
    phone = models.CharField(max_length=25, default='', null=True, blank=True)
    address = models.CharField(max_length=100, default='', null=True, blank=True)
    email = models.CharField(max_length=50, default='', null=True, blank=True)
    emergency_contact = models.CharField(max_length=100, null=True, blank=True)
    account_type = models.CharField(max_length=40, null=True, blank=True)
    user = models.IntegerField(default=1, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('acct-delete', kwargs={'id': self.id})

    def __unicode__(self):
        return 't_accts {}'.format(self.id)         

class t_employee_attribute(models.Model):

    rootid = models.ForeignKey(t_accts, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=15, null=True, blank=True)
    doh = models.CharField(max_length=15, null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True)
    user = models.IntegerField(default=1, null=True, blank=True)

    def __unicode__(self):
        return 't_employee_attribute {}'.format(self.id)    

class t_client_attribute(models.Model):

    rootid = models.ForeignKey(t_accts, on_delete=models.CASCADE)
    client_number = models.CharField(max_length=15, null=True, blank=True)
    company = models.CharField(max_length=50, null=True, blank=True)
    soc = models.DateField()
    status = models.CharField(max_length=10, null=True, blank=True)
    user = models.IntegerField(default=1, null=True, blank=True)

    def __unicode__(self):
        return 't_client_attribute {}'.format(self.id)  


class t_evaluation(models.Model):
    rootid = models.ForeignKey(t_accts, on_delete=models.CASCADE, default='1')
    employee_id = models.IntegerField(null=True, blank=True)
    scheduled_date = models.DateField()
    evaluated_date = models.DateField()
    status = models.CharField(max_length=10, null=True, blank=True)
    user = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now=False)
    updated = models.DateTimeField(auto_now_add = False, auto_now=True)

    def __unicode__(self):
        return 't_visit_tracker {}'.format(self.id)        
