# Generated by Django 3.0.4 on 2020-03-18 20:39

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('stu_dashboard', '0012_auto_20200319_0207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='sub_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='stu_dashboard.Subject'),
        ),
        migrations.AlterField(
            model_name='project_rules',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 25, 20, 38, 52, 115618, tzinfo=utc)),
        ),
    ]