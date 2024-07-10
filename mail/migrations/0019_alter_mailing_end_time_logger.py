# Generated by Django 4.2 on 2024-07-10 18:28

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mail", "0018_alter_mailing_end_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="end_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 7, 11, 18, 28, 25, 954750, tzinfo=datetime.timezone.utc
                ),
                verbose_name="конец рассылки",
            ),
        ),
        migrations.CreateModel(
            name="Logger",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_time_sending",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Время рассылки"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[(True, "Успешно"), (False, "Неудача")],
                        default=False,
                        max_length=30,
                        null=True,
                        verbose_name="Попытка",
                    ),
                ),
                (
                    "mailing",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mail.mailing",
                        verbose_name="Рассылка",
                    ),
                ),
            ],
            options={
                "verbose_name": "Лог",
                "verbose_name_plural": "Логи",
            },
        ),
    ]
