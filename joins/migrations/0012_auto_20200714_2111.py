# Generated by Django 2.0 on 2020-07-14 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joins', '0011_auto_20200714_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_accts',
            name='status',
            field=models.CharField(blank=True, choices=[('Active', 'Active'), ('NoneActive', 'NoneActive')], max_length=20, null=True),
        ),
    ]