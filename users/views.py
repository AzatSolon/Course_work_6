import random

from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, resolve_url, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView


from users.forms import UserRegisterForm, UserProfileForm
from users.models import User

CHARS = "abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"


class RegisterView(CreateView):
    """
    Контроллер создания(регистрации) пользователя
    """

    model = User
    form_class = UserRegisterForm
    template_name = "users/user_register.html"
    success_url = reverse_lazy("mail:home")

    def form_valid(self, form):
        token = ""
        for i in range(10):
            token += random.choice(CHARS)
        form.verified_pass = token
        user = form.save()
        user.token = token
        user.is_active = False
        send_mail(
            subject="Верификация почты",
            message=f"Поздравляем с регистрацией в сервисе Рассылки \n"
            f"Для завершения регистрации перейдите по ссылке: \n"
            f"http://127.0.0.1:8000/users/confirm/{user.token} \n"
            f"Если вы не причастны к регистации - игнорируйте это письмо.\n"
            f"С Уважением, команда Рассылки",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def verify_view(request, token):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
    user = User.objects.get(token=token)
    user.is_active = True
    user.save()
    return render(request, "users/user_verify.html")


def res_password(request):
    new_password = ""
    if request.method == "POST":
        email = request.POST["email"]
        user = get_object_or_404(User, email=email)
        for i in range(10):
            new_password += random.choice(CHARS)
        send_mail(
            subject="Смена пароля",
            message=f"Ваш новый пароль {new_password}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        user.set_password(new_password)
        user.save()
        return redirect(reverse("users:login"))
    return render(request, "users/password_recovery.html")


class ProfileView(UpdateView):
    """
    Контроллер профиля
    """

    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(PermissionRequiredMixin, ListView):
    """
    Контролер просмотра пользователей
    """

    model = User
    permission_required = "users.view_all_users"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = super().get_queryset().exclude(pk=user.pk)
        else:
            queryset = (
                super()
                .get_queryset()
                .exclude(pk=user.pk)
                .exclude(is_superuser=True)
                .exclude(is_staff=True)
            )
        return queryset


class UserDetailView(DetailView):
    """
    Контроллер просмотра одного пользователя
    """

    model = User


class MyLogoutView(LogoutView):
    """
    Контроллер для выхода из системы с помощью GET
    """

    http_method_names = ["get", "post", "options"]

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def my_logout_then_login(request, login_url=None):
    """
    Перенаправляет после выхода на страницу регистрации
    """
    login_url = resolve_url(login_url or settings.LOGIN_URL)
    return MyLogoutView.as_view(next_page=login_url)(request)
