# Generated by Django 2.2.6 on 2019-11-08 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libs', '0024_auto_20191108_0737'),
        ('joins', '0020_t_client_attribute_company'),
    ]

    operations = [
        migrations.DeleteModel(
            name='t_acct',
        ),
    ]
