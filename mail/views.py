import csv
from random import sample

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    TemplateView,
)

from blog.models import Blog
from mail.forms import ClientForm, MessageForm, MailingForm, MailingManagerForm
from mail.models import Mailing, Client, Message, Attempt


class MailingListView(LoginRequiredMixin, ListView):
    """
    Контроллер списка рассылок
    """

    model = Mailing

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name="manager"):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MailingDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер детального просмотра рассылки
    """

    model = Mailing
    success_url = reverse_lazy("mail:base")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if (
            not user.is_superuser
            and not user.groups.filter(name="manager")
            and user != self.object.owner
        ):
            raise PermissionDenied
        else:
            return self.object


class MailingCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер создания рассылки
    """

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mail:mailing_list")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        self.object.owner = user

    def get_form_kwargs(self):
        kwargs = super(MailingCreateView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingListViewSend(ListView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Письма"
        context["mail_count"] = self.get_queryset().count()
        return context


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер редактирования рассылки
    """

    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse_lazy("mail:mailing", args=[self.kwargs.get("pk")])

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingForm
        if user.has_perm("mail.complete_mailing"):
            return MailingManagerForm
        raise PermissionDenied

    def get_form_kwargs(self):
        kwargs = super(MailingUpdateView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер удаления рассылки
    """

    model = Mailing
    success_url = reverse_lazy("mail:mailing_list")


class ClientListView(LoginRequiredMixin, ListView):
    """
    Контроллер списка клиентов
    """

    model = Client

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(owner=user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер детального просмотра клиента
    """

    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер создания клиента
    """

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mail:client_list")

    def form_valid(self, form):
        client = form.save()
        client.owner = self.request.user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер редактирования клиента
    """

    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse_lazy("mail:client", args=[self.kwargs.get("pk")])


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер удаления клиента
    """

    model = Client
    success_url = reverse_lazy("mail:client_list")


class MessageListView(LoginRequiredMixin, ListView):
    """
    Контроллер списка сообщений
    """

    model = Message

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(owner=user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер детального просмотра сообщения
    """

    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер создания сообщения
    """

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mail:message_list")

    def form_valid(self, form):
        message = form.save()
        message.owner = self.request.user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер редактирования сообщения
    """

    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse_lazy("mail:message", args=[self.kwargs.get("pk")])


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер удаления сообщения
    """

    model = Message
    success_url = reverse_lazy("mail:message_list")


class HomePage(TemplateView):
    """
    Контроллер домашней страницы
    """

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["mailing_count"] = Mailing.objects.all().count()
        context_data["active_mailing_count"] = Mailing.objects.filter(
            status__in=["CREATED", "IN_PROGRESS"]
        ).count()
        context_data["unique_clients_count"] = (
            Client.objects.all().distinct("email").count()
        )
        all_posts = list(Blog.objects.all())
        context_data["random_posts"] = sample(all_posts, min(len(all_posts), 3))
        return context_data


class AttemptListView(LoginRequiredMixin, ListView):
    """
    Контроллер списка попыток отправки
    """

    model = Attempt

    def get_queryset(self):
        queryset = super().get_queryset()
        mailing_pk = self.kwargs.get("pk")
        queryset = queryset.filter(mailing__pk=mailing_pk)
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        mailing_pk = self.kwargs.get("pk")
        context_data["mailing"] = Mailing.objects.get(pk=mailing_pk)
        return context_data


class ContactsTemplateView(TemplateView):
    template_name = "contacts.html"

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name", "")
        phone = request.POST.get("phone", "")
        message = request.POST.get("message", "")
        print(f"{name} ({phone}) написал: {message}")

        with open("contact_info.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, phone, message])

        return HttpResponseRedirect(self.request.path)
