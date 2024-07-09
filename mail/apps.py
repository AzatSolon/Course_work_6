import os

from django.apps import AppConfig


class MailConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mail"

    def ready(self):
        if os.environ.get("RUN_MAIN") == "True":
            from mail.services import start_scheduler

            start_scheduler()
