# Generated by Django 4.2 on 2024-07-11 11:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mail", "0021_alter_mailing_end_time_alter_mailing_next_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="end_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 7, 12, 11, 9, 30, 976993, tzinfo=datetime.timezone.utc
                ),
                verbose_name="конец рассылки",
            ),
        ),
        migrations.AlterField(
            model_name="mailing",
            name="next_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 7, 11, 13, 9, 30, 976993, tzinfo=datetime.timezone.utc
                ),
                verbose_name="дата следующей рассылки",
            ),
        ),
    ]
