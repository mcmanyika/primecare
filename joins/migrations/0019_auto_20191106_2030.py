# Generated by Django 2.2.6 on 2019-11-06 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joins', '0018_t_evaluation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_accts',
            name='fname',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='t_accts',
            name='lname',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='t_accts',
            name='middle_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
