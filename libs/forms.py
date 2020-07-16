from django import forms
from libs.models import *
from joins.models import *



class ResourceForm(forms.ModelForm):
    class Meta:
        model = t_resources
        fields = ["name", "description", "document", 'category', 'user']
