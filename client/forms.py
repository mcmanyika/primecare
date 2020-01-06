from django import forms
from client.models import *

class AddClientForm(forms.ModelForm):
    class Meta:
        model = t_client
        fields = [  "fname", 
        			"middle_name", 
        			"lname",
        			"gender",
        			"dob",
        			"client_number",
        			"user",

        			] 

class CareGiverForm(forms.ModelForm):
    class Meta:
        model = t_care_giver
        fields = [  "client", 
        			"care_attendant",
        			"user",

        			] 

class BillForm(forms.ModelForm):
    class Meta:
        model = t_bill
        fields = [  
                    "rootid", 
                    "billing_date",
                    "batch_id",
                    "user",

                    ] 

class BatchForm(forms.ModelForm):
    class Meta:
        model = t_batch
        fields = [  "rootid", 
                    "billing_date",
                    "payment_date",
                    "notes",
                    "status",
                    "user",

                    ] 

class BillingTrackerForm(forms.ModelForm):
    class Meta:
        model = t_billing_tracker
        fields = [  "rootid", 
                    "claim_id",
                    "service_date_from",
                    "service_date_to",
                    "amount_billed",
                    "amount_paid",
                    "notes",
                    "payment_status", 
                    "client_number", 
                    "user"
                    ] 
class EditBillingTrackerForm(forms.ModelForm):
    class Meta:
        model = t_billing_tracker
        fields = [  "rootid", 
                    "amount_billed",
                    "amount_paid",
                    "notes",
                    "payment_status", 
                    "user"
                    ]                     