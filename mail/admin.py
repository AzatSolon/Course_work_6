from django.contrib import admin

from mail.models import Client, Mailing, Message, Logger


# Register your models here.


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "email")
    search_fields = ("email", "name")


@admin.register(Mailing)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ("id", "regularity", "start_time", "end_time", "status")
    search_fields = ("client", "status")
    list_filter = ("status",)


@admin.register(Message)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ("id", "subject")
    search_fields = ("subject", "text")


@admin.register(Logger)
class LoggerAdmin(admin.ModelAdmin):
    list_display = ("id", "mailing", "last_time_sending", "status")
    search_fields = ("mailing",)
