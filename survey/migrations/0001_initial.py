# Generated by Django 2.2.10 on 2020-07-03 18:28

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='t_questionnaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.BooleanField()),
                ('answer1', multiselectfield.db.fields.MultiSelectField(choices=[('Fever of 100 F (37.8 C) or above or possible fever symptoms like alternating chills and sweating', 'Fever of 100 F (37.8 C) , above or possible fever symptoms like alternating chills and sweating'), ('Cough', 'Cough'), ('Trouble breathing or shortness of breath or severe wheezing', 'Trouble breathing, shortness of breath or severe wheezing'), ('Chills or repeated shaking with chills', 'Chills, repeated shaking with chills'), ('Muscle aches', 'Muscle aches'), ('Sore throat', 'Sore throat'), ('Loss of smell or taste or a change in taste', 'Loss of smell or taste, or a change in taste'), ('Nausea or vomiting or diarrhea', 'Nausea, vomiting or diarrhea'), ('Headache', 'Headache'), ('None of the above', 'None of the above')], max_length=328)),
                ('user', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
