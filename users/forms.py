from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordResetForm,
)
from django import forms

from users.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text="Обязтельно для ввода")

    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
        )


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "email",
            "name",
            "last_name",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password"].widget = forms.HiddenInput()


class UserPassRecoveryForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "class": "form-control",
                "placeholder": "Введите ваш email",
            }
        ),
    )
