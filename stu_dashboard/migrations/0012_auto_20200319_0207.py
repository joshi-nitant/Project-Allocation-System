# Generated by Django 3.0.4 on 2020-03-18 20:37

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('stu_dashboard', '0011_auto_20200319_0024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project_rules',
            name='sub_id',
        ),
        migrations.AddField(
            model_name='project',
            name='sub_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='stu_dashboard.Subject'),
        ),
        migrations.AlterField(
            model_name='project_rules',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 25, 20, 37, 33, 619598, tzinfo=utc)),
        ),
    ]
