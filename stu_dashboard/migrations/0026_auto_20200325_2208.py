# Generated by Django 3.0.4 on 2020-03-25 16:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('stu_dashboard', '0025_auto_20200325_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_rules',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 1, 16, 38, 4, 433574, tzinfo=utc)),
        ),
    ]