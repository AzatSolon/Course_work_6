import logging
from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from mail.models import Mailing, Logger

logger = logging.getLogger(__name__)


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def my_job():
    day = timedelta(days=1)
    week = timedelta(days=7)
    month = timedelta(days=31)

    zone = pytz.timezone(settings.TIME_ZONE)
    today = datetime.now(zone)
    mailings = Mailing.objects.all()

    for mailing in mailings:
        if mailing.status != "Завершено" and mailing.status != "Создана":
            mailing.status = "Активна"
            mailing.save()
            emails_list = [client.email for client in mailing.client.all()]

            print(
                f"Рассылка {mailing.id} - начало {mailing.start_time}; конец {mailing.end_time}"
            )

            result = send_mail(
                subject=mailing.message.subject,
                message=mailing.message.text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=emails_list,
            )
            print("Рассылка Активна")

            status = result == True

            log = Logger(mailing=mailing, status=status)
            log.save()

            if mailing.regularity == "DAILY":
                mailing.next_date = log.last_time_sending + day
            elif mailing.regularity == "WEEKLY":
                mailing.next_date = log.last_time_sending + week
            elif mailing.regularity == "MONTHLY":
                mailing.next_date = log.last_time_sending + month

            if status:  # на случай сбоя рассылки
                if mailing.next_date < mailing.end_time:
                    mailing.status = "STATUS_CREATED"
                else:
                    mailing.status = "STATUS_COMPLETED"

            mailing.save()
            print(
                f"Рассылка {mailing.message} отправлена {today} (должна была {mailing.next_date})"
            )


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(minute="*/1"),  # Every 1 minute
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("send_message")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
