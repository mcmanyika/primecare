# Generated by Django 2.0 on 2020-07-11 16:37

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
                ('q1', models.BooleanField()),
                ('q2', models.BooleanField()),
                ('q3', models.BooleanField()),
                ('q4', models.BooleanField()),
                ('q5', multiselectfield.db.fields.MultiSelectField(choices=[('Fever of 100 F (37.8 C)', 'Fever (if measured with a thermometer)'), ('Cough', 'Cough'), ('Shortness of Breath or difficulty breathing', 'Shortness of Breath or difficulty breathing'), ('Chills', 'Chills'), ('Muscle aches', 'Muscle or body aches'), ('Sore throat', 'Sore throat'), ('New loss of taste or smell', 'New loss of taste or smell'), ('Nausea and vomiting', 'Nausea and vomiting'), ('Headache', 'Headache'), ('Diarrhea', 'Diarrhea'), ('Fatigue', 'Fatigue'), ('New onset of congestion or runny nose', 'New onset of congestion or runny nose'), ('None of the above', 'None of the above')], max_length=234)),
                ('q6', models.BooleanField()),
                ('q7', models.BooleanField()),
                ('user', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]