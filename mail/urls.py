from django.urls import path

from mail.apps import MailConfig
from mail.views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView, \
    ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView, MessageListView, \
    MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView, AttemptListView

app_name = MailConfig.name

urlpatterns = (
    path('', ClientListView.as_view(), name='home'),

    path('mail/', MailingListView.as_view(), name='mailing_list'),
    path('mail/<int:pk>/', MailingDetailView.as_view(), name='mailing'),
    path('mail/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mail/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mail/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
    path('mail/<int:pk>/attempt/', AttemptListView.as_view(), name='attempt_list'),
)
