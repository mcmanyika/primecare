# Generated by Django 2.0 on 2020-07-16 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libs', '0002_t_dict_use'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='t_dict',
            name='use',
        ),
    ]
