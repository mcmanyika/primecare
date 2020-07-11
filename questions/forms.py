from django import forms
from .models import *


class CovidForm(forms.ModelForm):
    class Meta:
        model = t_questionnaire
        fields = ["q1", "q2", "q3", "q4", "q5", "q6", "q7", "user"]
