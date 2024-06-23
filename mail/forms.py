from django.forms import ModelForm

from mail.models import Client, Message, Mailing
from django.forms import BooleanField


class StyleMixin:
    """
    Миксин стилизации форм
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ClientForm(StyleMixin, ModelForm):
    """
    Форма для редактирования клиента
    """

    class Meta:
        model = Client
        fields = ["name", "email", "comment"]
        exclude = ("owner",)


class MessageForm(StyleMixin, ModelForm):
    """
    Форма для редактирования сообщения
    """

    class Meta:
        model = Message
        fields = ["subject", "text"]


class MailingForm(StyleMixin, ModelForm):
    """
    Форма для редактирования рассылки
    """

    class Meta:
        model = Mailing
        exclude = (
            "next_send_time",
            "owner",
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields["client"].queryset = Client.objects.filter(owner=user)
        self.fields["message"].queryset = Message.objects.filter(owner=user)


class MailingManagerForm(StyleMixin, ModelForm):
    """
    Форма редактирования рассылки менеджером
    """

    class Meta:
        model = Mailing
        fields = ("owner",)
