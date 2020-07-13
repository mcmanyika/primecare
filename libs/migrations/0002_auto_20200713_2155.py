# Generated by Django 2.0 on 2020-07-13 21:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('libs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='t_accts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('dob', models.CharField(blank=True, max_length=15, null=True)),
                ('phone', models.CharField(blank=True, default='', max_length=25, null=True)),
                ('address', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('email', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('emergency_contact', models.CharField(blank=True, max_length=100, null=True)),
                ('account_type', models.CharField(blank=True, max_length=40, null=True)),
                ('status', models.CharField(blank=True, max_length=10, null=True)),
                ('user', models.IntegerField(blank=True, default=1, null=True)),
                ('rootid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='t_oig',
            name='rootid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libs.t_accts'),
        ),
        migrations.AlterField(
            model_name='t_visit_tracker',
            name='rootid',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='libs.t_accts'),
        ),
    ]