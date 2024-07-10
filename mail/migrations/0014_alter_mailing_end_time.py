# Generated by Django 4.2 on 2024-07-09 05:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mail", "0013_alter_mailing_end_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="end_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 7, 10, 5, 24, 44, 912029, tzinfo=datetime.timezone.utc
                ),
                verbose_name="конец рассылки",
            ),
        ),
    ]