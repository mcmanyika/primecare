
from multiselectfield import MultiSelectField

from django.db import models

# Create your models here.


class t_questionnaire(models.Model):
    QUESTION_CHOCES = (
        ('Fever of 100 F (37.8 C)',
         'Fever (if measured with a thermometer)'),
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
        ('New onset of congestion or runny nose',
         'New onset of congestion or runny nose'),
        ('None of the above', 'None of the above')
    )
    answer = models.BooleanField()
    answer1 = MultiSelectField(choices=QUESTION_CHOCES)
    user = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return 't_questionnaire {}'.format(self.id)