# Generated by Django 4.2 on 2024-07-09 06:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mail", "0015_alter_mailing_end_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="end_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 7, 10, 6, 16, 41, 570893, tzinfo=datetime.timezone.utc
                ),
                verbose_name="конец рассылки",
            ),
        ),
    ]