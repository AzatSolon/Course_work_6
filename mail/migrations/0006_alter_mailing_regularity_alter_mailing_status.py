# Generated by Django 5.0.6 on 2024-06-27 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mail", "0005_attempt_client_alter_attempt_attempt_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="regularity",
            field=models.CharField(
                choices=[("D", "daily"), ("W", "weekly"), ("M", "monthly")],
                default="D",
                max_length=30,
                verbose_name="Периодичность",
            ),
        ),
        migrations.AlterField(
            model_name="mailing",
            name="status",
            field=models.CharField(
                choices=[("CR", "Создана"), ("ON", "В процессе"), ("OFF", "Завершена")],
                default="CR",
                max_length=30,
                verbose_name="Статус",
            ),
        ),
    ]
