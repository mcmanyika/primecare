# Generated by Django 2.0 on 2020-07-14 22:04

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0007_auto_20200713_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_questionnaire',
            name='q5',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Cough', 'Cough'), ('Shortness of Breath or difficulty breathing', 'Shortness of Breath or difficulty breathing'), ('Chills', 'Chills'), ('Muscle aches', 'Muscle or body aches'), ('Sore throat', 'Sore throat'), ('New loss of taste or smell', 'New loss of taste or smell'), ('Nausea and vomiting', 'Nausea and vomiting'), ('Headache', 'Headache'), ('Diarrhea', 'Diarrhea'), ('Fatigue', 'Fatigue'), ('New onset of congestion or runny nose', 'New onset of congestion or runny nose'), ('None of the above', 'None of the above')], max_length=210, null=True),
        ),
    ]