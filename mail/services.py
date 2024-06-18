import datetime
import smtplib

import pytz
from django.core.mail import send_mail

from config import settings
from mailing.models import Mailing, Attempt


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
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client.email for client in mailing.clients.all()],
            fail_silently=False,
        )
        if response == 1:
            # При успешной отправке сохраняем информацию о попытке в базу данных
            mailing.status = 'IN_PROGRESS'
            server_response = 'Успешно отправлено'
            Attempt.objects.create(
                status=Attempt.ATTEMPT_SUCCESS, response=server_response, mailing=mailing)

            # Устанавливаем дату следующей отправки письма
            if mailing.periodicity == 'DAILY':
                mailing.start_mailing += datetime.timedelta(days=1)
            elif mailing.periodicity == 'WEEKLY':
                mailing.start_mailing += datetime.timedelta(days=7)
            elif mailing.periodicity == 'MONTHLY':
                mailing.start_mailing += datetime.timedelta(days=30)

            mailing.save()

    except smtplib.SMTPException as error:
        # При ошибке отправки записываем полученный ответ сервера
        Attempt.objects.create(status=Attempt.ATTEMPT_FAIL, response=error, mailing=mailing)


def send_scheduled_mail():
    """
    Проверяет, какие рассылки должны быть завершены,
    а какие необходимо отправить в данный момент времени,
    и осуществляет их отправку
    """
    current_datetime = datetime.datetime.now(pytz.timezone(settings.TIME_ZONE))

    # Проверяем, какие рассылки должны быть завершены в этот момент времени
    for mailing in Mailing.objects.filter(status='IN_PROGRESS').filter(end_mailing__lt=current_datetime):
        mailing.status = 'COMPLETED'
        mailing.save()
    # Проверяем, какие рассылки должны быть отправлены в этот момент времени и производим отправку
    mailings = Mailing.objects.filter(status__in=['CREATED', 'IN_PROGRESS']).filter(start_mailing__lte=current_datetime)
    for mailing in mailings:
        mailing.status = 'IN_PROGRESS'
        mailing.save()
        send_message(mailing)
    print('Mailing completed')
