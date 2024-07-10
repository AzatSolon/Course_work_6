from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {"blank": True, "null": True}

LOG_CHOICES = (
    (True, "Успешно"),
    (False, "Неудача"),
)


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
    Модель сообщения рассылки
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
        return f"{self.subject} : {self.text}"

    class Meta:
        verbose_name = "сообщение для рассылки"
        verbose_name_plural = "сообщения для рассылки"


class Mailing(models.Model):
    """
    Модель рассылки
    """

    EVERY_TWO_HOURS = "Каждые 2 часа"
    DAILY = "Ежедневно"
    WEEKLY = "Еженедельно"
    MONTHLY = "Ежемесечно"

    PERIODS = [
        (EVERY_TWO_HOURS, "Каждые 2 часа"),
        (DAILY, "Ежедневно"),
        (WEEKLY, "Еженедельно"),
        (MONTHLY, "Ежемесечно"),
    ]

    STATUS_CREATED = "Создана"
    STATUS_STARTED = "Активна"
    STATUS_COMPLETED = "Завершено"

    STATUS = [
        (STATUS_CREATED, "Создана"),
        (STATUS_STARTED, "Активна"),
        (STATUS_COMPLETED, "Завершено"),
    ]

    start_time = models.DateTimeField(
        default=timezone.now, verbose_name="начало рассылки"
    )
    end_time = models.DateTimeField(
        default=(timezone.now() + timezone.timedelta(days=1)),
        verbose_name="конец рассылки",
    )
    regularity = models.CharField(
        max_length=30,
        choices=PERIODS,
        verbose_name="Периодичность",
    )
    next_date = models.DateTimeField(
        default=(timezone.now() + timezone.timedelta(hours=2)),
        verbose_name="дата следующей рассылки",
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS,
        default="created",
        verbose_name="Статус",
    )
    message = models.OneToOneField(
        Message, on_delete=models.CASCADE, verbose_name="Сообщение"
    )
    client = models.ManyToManyField(Client, verbose_name="Клиенты")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="пользователь", **NULLABLE
    )

    def __str__(self):
        return f"{self.regularity} ({self.message})."

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


class Logger(models.Model):
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, verbose_name="Рассылка", **NULLABLE
    )
    last_time_sending = models.DateTimeField(
        auto_now=True, verbose_name="Время рассылки", **NULLABLE
    )
    status = models.CharField(
        default=False,
        max_length=30,
        choices=LOG_CHOICES,
        verbose_name="Попытка",
        **NULLABLE,
    )

    def __str__(self):
        return f"{self.last_time_sending} - {self.status}"

    class Meta:
        verbose_name = "Лог"
        verbose_name_plural = "Логи"
