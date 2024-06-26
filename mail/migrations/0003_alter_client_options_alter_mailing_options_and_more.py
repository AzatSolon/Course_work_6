# Generated by Django 5.0.6 on 2024-06-21 11:13

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mail", "0002_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="client",
            options={"verbose_name": "клиент", "verbose_name_plural": "клиенты"},
        ),
        migrations.AlterModelOptions(
            name="mailing",
            options={
                "permissions": [
                    ("deactivate_mailing", "Can deactivate mailing"),
                    ("view_all_mailings", "Can view all mailings"),
                ],
                "verbose_name": "рассылка",
                "verbose_name_plural": "рассылки",
            },
        ),
        migrations.AlterModelOptions(
            name="message",
            options={
                "verbose_name": "сообщение для рассылки",
                "verbose_name_plural": "сообщения для рассылки",
            },
        ),
        migrations.RemoveField(
            model_name="client",
            name="owner",
        ),
        migrations.RemoveField(
            model_name="client",
            name="comments",
        ),
        migrations.RemoveField(
            model_name="mailing",
            name="owner",
        ),
        migrations.RemoveField(
            model_name="mailing",
            name="clients",
        ),
        migrations.RemoveField(
            model_name="mailing",
            name="end_mailing",
        ),
        migrations.RemoveField(
            model_name="mailing",
            name="periodicity",
        ),
        migrations.RemoveField(
            model_name="mailing",
            name="start_mailing",
        ),
        migrations.RemoveField(
            model_name="message",
            name="owner",
        ),
        migrations.AddField(
            model_name="client",
            name="comment",
            field=models.TextField(
                blank=True, max_length=250, null=True, verbose_name="Комментарий"
            ),
        ),
        migrations.AddField(
            model_name="client",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
        migrations.AddField(
            model_name="client",
            name="patronymic",
            field=models.CharField(
                blank=True, max_length=150, null=True, verbose_name="Отчество"
            ),
        ),
        migrations.AddField(
            model_name="client",
            name="surname",
            field=models.CharField(
                blank=True, max_length=150, null=True, verbose_name="Фамилия"
            ),
        ),
        migrations.AddField(
            model_name="mailing",
            name="client",
            field=models.ManyToManyField(to="mail.client", verbose_name="клиент"),
        ),
        migrations.AddField(
            model_name="mailing",
            name="next_send_time",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="следущая рассылка"
            ),
        ),
        migrations.AddField(
            model_name="mailing",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
        migrations.AddField(
            model_name="mailing",
            name="regularity",
            field=models.CharField(
                blank=True,
                choices=[
                    ("daily", "раз в день"),
                    ("weekly", "раз в неделю"),
                    ("monthly", "раз в месяц"),
                ],
                max_length=50,
                null=True,
                verbose_name="периодичность",
            ),
        ),
        migrations.AddField(
            model_name="mailing",
            name="start_time",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="дата и время рассылки"
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="mailing_images/",
                verbose_name="картинка",
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
        migrations.AlterField(
            model_name="client",
            name="email",
            field=models.EmailField(max_length=254, verbose_name="email"),
        ),
        migrations.AlterField(
            model_name="client",
            name="name",
            field=models.CharField(max_length=150, verbose_name="Имя"),
        ),
        migrations.AlterField(
            model_name="mailing",
            name="message",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="mail.message",
                verbose_name="сообщение",
            ),
        ),
        migrations.AlterField(
            model_name="mailing",
            name="status",
            field=models.CharField(
                choices=[
                    ("created", "создана"),
                    ("completed", "завершена"),
                    ("started", "запущена"),
                ],
                default="created",
                max_length=50,
                verbose_name="статус рассылки",
            ),
        ),
        migrations.AlterField(
            model_name="message",
            name="subject",
            field=models.CharField(max_length=150, verbose_name="тема письма"),
        ),
        migrations.AlterField(
            model_name="message",
            name="text",
            field=models.TextField(verbose_name="сообщение"),
        ),
    ]
