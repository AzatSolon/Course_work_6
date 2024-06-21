from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """
    Модель клиента
    """
    email = models.EmailField(verbose_name='email')
    name = models.CharField(max_length=150, verbose_name='Имя')
    surname = models.CharField(max_length=150, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=150, verbose_name='Отчество')
    comment = models.TextField(verbose_name='комментарий')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)

    def __str__(self):
        return f'{self.surname} {self.name}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    """
    Модель сообщения
    """
    subject = models.CharField(max_length=150, verbose_name='тема письма')
    message = models.TextField(verbose_name='сообщение')

    image = models.ImageField(upload_to='mailing_images/', **NULLABLE, verbose_name='картинка')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'сообщение для рассылки'
        verbose_name_plural = 'сообщения для рассылки'


class Mailing(models.Model):
    """
    Модель Рассылки
    """
    CREATED = 'created'
    COMPLETED = 'completed'
    STARTED = 'started'
    STATUS_VARIANTS = [
        (CREATED, 'создана'),
        (COMPLETED, 'завершена'),
        (STARTED, 'запущена'),
    ]

    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    REGULARITY_VARIANTS = [
        (DAILY, 'раз в день'),
        (WEEKLY, 'раз в неделю'),
        (MONTHLY, 'раз в месяц'),
    ]
    start_time = models.DateTimeField(verbose_name='дата и время рассылки')
    regularity = models.CharField(max_length=50, choices=REGULARITY_VARIANTS, verbose_name='периодичность')

    status = models.CharField(max_length=50, choices=STATUS_VARIANTS, default=CREATED, verbose_name='статус рассылки')

    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение')
    client = models.ManyToManyField(Client, verbose_name='клиент')

    next_send_time = models.DateTimeField()

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)

    def save(self, *args, **kwargs):
        if not self.next_send_time:
            self.next_send_time = self.start_time
        super().save(*args, **kwargs)

    def __str__(self):
        return self.message.subject

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        permissions = [
            ('deactivate_mailing', 'Can deactivate mailing'),
            ('view_all_mailings', 'Can view all mailings'),
        ]


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
