# Generated by Django 3.0.4 on 2020-03-25 11:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('stu_dashboard', '0023_auto_20200323_1644'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teaches',
            old_name='fac_id',
            new_name='fac_id_id',
        ),
        migrations.AddField(
            model_name='project',
            name='is_admin',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='project_rules',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 1, 11, 35, 59, 259835, tzinfo=utc)),
        ),
    ]