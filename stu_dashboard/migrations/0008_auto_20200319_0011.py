# Generated by Django 3.0.4 on 2020-03-18 18:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('stu_dashboard', '0007_auto_20200319_0008'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='site_user',
            new_name='s_id',
        ),
        migrations.AlterField(
            model_name='project_rules',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 25, 18, 41, 29, 797014, tzinfo=utc)),
        ),
    ]