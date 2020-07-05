from django import forms
from .models import *


class CovidForm(forms.ModelForm):
    class Meta:
        model = t_questionnaire
        fields = ["answer", "answer1", "user"]
