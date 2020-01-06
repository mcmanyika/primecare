from __future__ import unicode_literals
from django.conf import settings
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse    
from django import forms 

# Create your models here.

class Snippets(models.Model):
    title = models.CharField(max_length=50,null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now=False)
    updated = models.DateTimeField(auto_now_add = False, auto_now=True)

    def __unicode__(self):
        return 'Snippets {}'.format(self.id)