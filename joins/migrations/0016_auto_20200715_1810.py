# Generated by Django 2.0 on 2020-07-15 18:10

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('questions', '0009_auto_20200715_1807'),
        ('client', '0002_auto_20200715_1807'),
        ('joins', '0015_delete_t_accts'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='t_accounts',
            new_name='t_accts',
        ),
    ]