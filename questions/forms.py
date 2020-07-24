from django import forms
from .models import *


class CovidForm(forms.ModelForm):
    class Meta:
        model = t_questionnaire
        fields = ["rootid", "q1", "q2", "q3",
                  "q4", "q5", "q6", "q7", "q8", "q9", "user"]
