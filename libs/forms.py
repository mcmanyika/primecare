from django import forms
from libs.models import *
from joins.models import *


class EmployeeSignInForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["Daily_Login_ID", "PatientID", 'user']


class EmployeeSignOutForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["Daily_Logout_ID", "PatientID",  'user']


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = t_evaluation
        fields = ["rootid", "employee_id", "scheduled_date",
                  "evaluated_date", "status",  'user']


class ExclusionForm(forms.ModelForm):
    class Meta:
        model = t_oig
        fields = ["root", "rootid", "site", "date", "document", 'user']


class ResourceForm(forms.ModelForm):
    class Meta:
        model = t_resources
        fields = ["name", "description", "document", 'category', 'user']
