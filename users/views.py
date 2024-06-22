from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LogoutView
from django.shortcuts import get_object_or_404, redirect, resolve_url
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView, UpdateView, ListView, DetailView

from mail.services import send_mail
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:register_success')
    object = None

    def get_success_url(self):
        return reverse_lazy('users:register_success')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_link = self.request.build_absolute_uri(reverse('users:toggle_activity'))

        user_email = user.email
        subject = "Подтверждение регистрации"
        message = f"Добро пожаловать! Подтвердите вашу регистрацию по следующей ссылке: {verification_link}?uid={uid}&token={token}"
        send_mail(subject, message, [user_email], newsletter=None)

        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.view_all_users'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = super().get_queryset().exclude(pk=user.pk)
        else:
            queryset = super().get_queryset().exclude(pk=user.pk).exclude(is_superuser=True).exclude(is_staff=True)
        return queryset


@permission_required('users.deactivate_user')
def toggle_activity(request, pk):
    user = User.objects.get(pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect(reverse('users:view_all_users'))


class UserDetailView(DetailView):
    model = User


class MyLogoutView(LogoutView):
    """
    класс для выхода из системы с помощью GET
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
