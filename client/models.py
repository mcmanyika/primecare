from django.db import models
from joins.models import *

# Create your models here.


class t_client(models.Model):

    fname = models.CharField(max_length=20, null=True, blank=True)
    middle_name = models.CharField(max_length=12, null=True, blank=True)
    lname = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    dob = models.CharField(max_length=15, null=True, blank=True)
    phone = models.CharField(max_length=25, default='', null=True, blank=True)
    address = models.CharField(
        max_length=100, default='', null=True, blank=True)
    ssn = models.CharField(max_length=25, null=True, blank=True)
    client_number = models.IntegerField(null=True, blank=True)
    soc = models.CharField(max_length=15, null=True, blank=True)
    emergency_contact = models.CharField(max_length=100, null=True, blank=True)
    user = models.IntegerField(default=1, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return 't_client {}'.format(self.id)


class t_care_giver(models.Model):
    client = models.ForeignKey(t_client, on_delete=models.CASCADE)
    care_attendant = models.IntegerField(default=1, null=True, blank=True)
    user = models.IntegerField(default=1, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return 't_care_giver {}'.format(self.id)


class t_bill(models.Model):
    rootid = models.IntegerField(null=True, blank=True)
    billing_date = models.CharField(max_length=50, default='')
    batch_id = models.CharField(max_length=50, default='')
    user = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return 't_bill {}'.format(self.id)


class t_batch(models.Model):
    rootid = models.ForeignKey(t_bill, on_delete=models.CASCADE)
    billing_date = models.DateField()
    payment_date = models.DateField(null=True, blank=True)
    notes = models.CharField(max_length=100, default='', null=True, blank=True)
    status = models.CharField(max_length=20, default='')
    user = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return 't_batch {}'.format(self.id)


class t_billing_tracker(models.Model):
    rootid = models.ForeignKey(t_accounts, on_delete=models.CASCADE)
    claim_id = models.CharField(
        max_length=50, default='', null=True, blank=True)
    service_date_from = models.DateField(null=True, blank=True)
    service_date_to = models.DateField(null=True, blank=True)
    amount_billed = models.IntegerField()
    amount_paid = models.IntegerField()
    notes = models.CharField(max_length=80, default='', null=True, blank=True)
    payment_status = models.CharField(
        max_length=20, default='', null=True, blank=True)
    client_number = models.IntegerField(null=True, blank=True)
    user = models.IntegerField(null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return 't_billing_tracker {}'.format(self.id)
