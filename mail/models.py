from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """
    Модель клиента
    """
    name = models.CharField(max_length=100, verbose_name='Ф.И.О.')
    email = models.EmailField(max_length=100, verbose_name='Email')
    comments = models.TextField(verbose_name='Комментарий')
    client_manager = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Клиентский менеджер', **NULLABLE)

    def __str__(self):
        return f'{self.email} ({self.name})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    """
    Модель сообщения для отправки
    """
    subject = models.CharField(max_length=100, verbose_name='Тема')
    text = models.TextField(verbose_name='Текст')
    client_manager = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Клиентский менеджер', **NULLABLE)

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    """
    Модель рассылки
    """

    PERIODICITY_CHOICES = [
        ('DAILY', 'Ежедневно'),
        ('WEEKLY', 'Еженедельно'),
        ('MONTHLY', 'Ежемесячно'),
    ]

    STATUS_CHOICES = [
        ('CREATED', 'Создана'),
        ('IN_PROGRESS', 'В процессе'),
        ('COMPLETED', 'Завершена'),
    ]

    start_mailing = models.DateTimeField(verbose_name='Начало рассылки')
    end_mailing = models.DateTimeField(verbose_name='Конец рассылки', **NULLABLE)
    periodicity = models.CharField(max_length=30, choices=PERIODICITY_CHOICES, verbose_name='Периодичность')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='CREATED', verbose_name='Статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты')
    client_manager = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Клиентский менеджер', **NULLABLE)

    def __str__(self):
        return f'С {self.start_mailing} {self.periodicity} ({self.status}).'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [('set_completed', 'Can complete mailing'), ]


class Attempt(models.Model):
    """
    Модель попытки отправки сообщения
    """
    ATTEMPT_SUCCESS = 'SUCCESS'
    ATTEMPT_FAIL = 'FAIL'

    ATTEMPT_CHOICES = [
        (ATTEMPT_SUCCESS, 'Успешно'),
        (ATTEMPT_FAIL, 'Неуспешно'),
    ]

    attempt_date = models.DateTimeField(verbose_name='Дата отправки', auto_now_add=True)
    status = models.CharField(max_length=50, choices=ATTEMPT_CHOICES, verbose_name='Статус отправки')
    response = models.TextField(verbose_name='Ответ сервера', **NULLABLE)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')

    def __str__(self):
        return f'{self.attempt_date} ({self.status})'

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'
