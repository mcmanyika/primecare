# Generated by Django 2.0 on 2020-07-11 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joins', '0007_auto_20200711_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_accts',
            name='rootid',
            field=models.IntegerField(blank=True, default=1000, null=True),
        ),
    ]
