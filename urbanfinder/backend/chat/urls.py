"""
Chat URL routes.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.ConversationListView.as_view(), name="chat-conversations"),
    path("start/", views.ConversationStartView.as_view(), name="chat-start"),
    path(
        "<uuid:conversation_id>/messages/",
        views.ConversationMessagesView.as_view(),
        name="chat-messages",
    ),
    path(
        "<uuid:conversation_id>/send/",
        views.SendMessageView.as_view(),
        name="chat-send",
    ),
]
