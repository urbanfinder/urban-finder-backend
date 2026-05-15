"""
Admin configuration for Chat.
"""

from django.contrib import admin

from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ["sender", "content", "is_read", "created_at"]


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ["initiator", "receiver", "related_property", "created_at"]
    search_fields = ["initiator__email", "receiver__email", "related_property__title"]
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["conversation", "sender", "content_preview", "is_read", "created_at"]
    list_filter = ["is_read", "created_at"]

    @admin.display(description="Content")
    def content_preview(self, obj):
        return obj.content[:80]
