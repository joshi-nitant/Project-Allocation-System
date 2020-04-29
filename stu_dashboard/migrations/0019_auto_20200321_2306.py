# Generated by Django 3.0.4 on 2020-03-21 17:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('stu_dashboard', '0018_auto_20200321_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_rules',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 28, 17, 36, 20, 550679, tzinfo=utc)),
        ),
        migrations.AlterUniqueTogether(
            name='team',
            unique_together={('leader_id_id', 'subject_id_id')},
        ),
    ]
