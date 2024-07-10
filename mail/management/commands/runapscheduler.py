import smtplib
from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand

from mail.models import Mailing, Attempt


class Command(BaseCommand):

    def handle(self, *args, **options):
        mailings = Mailing.objects.filter(status="Активна")

        for mailing in mailings:
            clients = mailing.clients.all()
            try:
                server_response = send_mail(
                    subject=mailing.message.title,
                    message=mailing.message.message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in clients],
                    fail_silently=False,
                )
                Attempt.objects.create(
                    status=Attempt.SUCCESS,
                    server_response=server_response,
                    mailing=mailing,
                )
            except smtplib.SMTPException as e:
                Attempt.objects.create(
                    status=Attempt.FAIL,
                    server_response=str(e),
                    mailing=mailing,
                )
