import smtplib
from datetime import datetime

from django.core.cache import cache
from django.core.mail import send_mail

from blog.models import Blog
from config import settings
from config.settings import EMAIL_HOST_USER
from mail.models import Attempt


def send_message(mailing):
    """
    Отправляет сообщение клиентам,
    содержащимся в списке рассылки и фиксирует ответ сервера,
    устанавливая дату следующей рассылки в зависимости от выбранной периодичности
    """
    subject = mailing.message.subject
    message = mailing.message.text
    try:
        response = send_mail(
            subject=subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[client.email for client in mailing.clients.all()],
            fail_silently=False,
        )
        if response == 1:
            # При успешной отправке сохраняем информацию о попытке в базу данных
            mailing.status = "IN_PROGRESS"
            server_response = "Успешно отправлено"
            Attempt.objects.create(
                status=Attempt.ATTEMPT_SUCCESS,
                response=server_response,
                mailing=mailing,
            )

            # Устанавливаем дату следующей отправки письма
            if mailing.regularity == "DAILY":
                mailing.start_mailing += datetime.timedelta(days=1)
            elif mailing.regularity == "WEEKLY":
                mailing.start_mailing += datetime.timedelta(days=7)
            elif mailing.regularity == "MONTHLY":
                mailing.start_mailing += datetime.timedelta(days=30)

            mailing.save()

    except smtplib.SMTPException as error:
        # При ошибке отправки записываем полученный ответ сервера
        Attempt.objects.create(
            status=Attempt.ATTEMPT_FAIL, response=error, mailing=mailing
        )


def get_cached_blogs():
    if settings.CACHE_ENABLED:
        key = "blog_list"
        blog_list = cache.get(key)
        if blog_list is None:
            blog_list = Blog.objects.all()
            cache.set(key, blog_list)
    else:
        blog_list = Blog.objects.all()

    return blog_list
