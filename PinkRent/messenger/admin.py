from django.contrib import admin
from .models import Conversation, Message

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('listing', 'sender', 'receiver', 'last_message', 'created_at')
    list_filter = ('sender', 'receiver', 'created_at')
    search_fields = ('sender__username', 'receiver__username')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'timestamp', 'read')
    list_filter = ('read', 'timestamp')
    search_fields = ('content',)
