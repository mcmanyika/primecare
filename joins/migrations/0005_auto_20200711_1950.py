# Generated by Django 2.0 on 2020-07-11 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('joins', '0004_auto_20200711_1949'),
    ]

    operations = [
        migrations.RenameField(
            model_name='t_accts',
            old_name='root',
            new_name='rootid',
        ),
    ]