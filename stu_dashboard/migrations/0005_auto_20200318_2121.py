# Generated by Django 3.0.4 on 2020-03-18 15:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('stu_dashboard', '0004_auto_20200318_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_rules',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 25, 15, 51, 2, 218059, tzinfo=utc)),
        ),
    ]
