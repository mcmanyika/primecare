
from multiselectfield import MultiSelectField

from django.db import models
from joins.models import *

# Create your models here.


class t_questionnaire(models.Model):
    QUESTION_CHOCE = (
        ('Cough', 'Cough'),
        ('Shortness of Breath or difficulty breathing',
         'Shortness of Breath or difficulty breathing'),
        ('Chills',
         'Chills'),
        ('Muscle aches', 'Muscle or body aches'),
        ('Sore throat', 'Sore throat'),
        ('New loss of taste or smell',
         'New loss of taste or smell'),
        ('Nausea and vomiting', 'Nausea and vomiting'),
        ('Headache', 'Headache'),
        ('Diarrhea', 'Diarrhea'),
        ('Fatigue', 'Fatigue'),
        ('New onset of congestion or runny nose',
         'New onset of congestion or runny nose'),
        ('None of the above', 'None of the above')
    )
    rootid = models.ForeignKey(
        t_acct, on_delete=models.CASCADE, default='1000')
    q1 = models.BooleanField()
    q2 = models.BooleanField()
    q3 = models.BooleanField()
    q4 = models.BooleanField()
    q5 = MultiSelectField(choices=QUESTION_CHOCE, null=True, blank=True)
    q6 = models.CharField(max_length=40)
    q7 = models.CharField(max_length=10)
    q8 = models.BooleanField()
    user = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return 't_questionnaire {}'.format(self.id)
