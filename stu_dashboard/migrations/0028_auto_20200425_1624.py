# Generated by Django 3.0.4 on 2020-04-25 10:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('stu_dashboard', '0027_auto_20200425_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_rules',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 2, 10, 54, 22, 479772, tzinfo=utc)),
        ),
    ]
