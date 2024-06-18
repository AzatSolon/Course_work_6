import secrets

from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        token = secrets.token_hex(16)
        self.object.token = token
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Здравствуйте, для подтверждения вашей почты перейдите по ссылке: {url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email],
        )

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
