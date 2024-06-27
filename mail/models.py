from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Client(models.Model):
    """
    Модель клиента
    """

    email = models.EmailField(verbose_name="email")
    name = models.CharField(max_length=150, verbose_name="Имя")
    surname = models.CharField(max_length=150, verbose_name="Фамилия", **NULLABLE)
    patronymic = models.CharField(max_length=150, verbose_name="Отчество", **NULLABLE)
    comment = models.TextField(max_length=250, verbose_name="Комментарий", **NULLABLE)

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="пользователь", **NULLABLE
    )

    def __str__(self):
        return f"{self.surname} {self.name}"

    class Meta:
        verbose_name = "Kлиент"
        verbose_name_plural = "Kлиенты"


class Message(models.Model):
    """
    Модель сообщения
    """

    subject = models.CharField(max_length=150, verbose_name="тема письма")
    text = models.TextField(verbose_name="сообщение")

    image = models.ImageField(
        upload_to="mailing_images/", **NULLABLE, verbose_name="картинка"
    )

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="пользователь", **NULLABLE
    )

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "сообщение для рассылки"
        verbose_name_plural = "сообщения для рассылки"


class Mailing(models.Model):
    """
    Модель рассылки
    """

    class MailingChoices(models.TextChoices):
        DAILY = "D", "daily"
        WEEKLY = "W", "weekly"
        MONTHLY = "M", "monthly"

    class StatusChoices(models.TextChoices):
        CREATED = "CR", "Создана"
        IN_PROGRESS = "ON", "В процессе"
        COMPLETED = "OFF", "Завершена"

    start_mailing = models.DateTimeField(
        default=timezone.now, verbose_name="Начало рассылки"
    )
    end_mailing = models.DateTimeField(verbose_name="Конец рассылки", **NULLABLE)
    regularity = models.CharField(
        max_length=30,
        choices=MailingChoices.choices,
        default=MailingChoices.DAILY,
        verbose_name="Периодичность",
    )
    status = models.CharField(
        max_length=30, choices=StatusChoices.choices, default=StatusChoices.CREATED, verbose_name="Статус"
    )
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name="Сообщение"
    )
    client = models.ManyToManyField(Client, verbose_name="Клиенты")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="пользователь", **NULLABLE
    )

    def __str__(self):
        return f"С {self.start_mailing} {self.regularity} ({self.status})."

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ("set_completed", "Can complete mailing"),
        ]


class Attempt(models.Model):
    """
    Модель попытки отправки сообщения
    """

    ATTEMPT_SUCCESS = "SUCCESS"
    ATTEMPT_FAIL = "FAIL"

    ATTEMPT_CHOICES = [
        (ATTEMPT_SUCCESS, "Успешно"),
        (ATTEMPT_FAIL, "Не успешно"),
    ]

    attempt_date = models.DateTimeField(verbose_name="Дата отправки")
    status = models.CharField(
        max_length=50,
        choices=ATTEMPT_CHOICES,
        default=ATTEMPT_FAIL,
        verbose_name="Статус отправки",
    )
    response = models.TextField(verbose_name="Ответ сервера", **NULLABLE)
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, verbose_name="Рассылка"
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f"{self.attempt_date} ({self.status})"

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"
