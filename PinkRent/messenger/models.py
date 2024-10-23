from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from listings.models import Listing

User = get_user_model()

class Conversation(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_conversations')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_conversations')
    
    last_message = models.ForeignKey('Message', on_delete=models.SET_NULL, null=True, blank=True, related_name='last_message_in_conversation')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Conversation {self.id} for {self.listing.name} between {self.sender.username} and {self.receiver.username}'

    class Meta:
        unique_together = ('listing', 'sender', 'receiver')  # Ensure unique conversation for the same sender, receiver, and listing
        ordering = ['created_at']

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True)  # Add receiver field
    content = models.TextField(_("Content"))
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver} at {self.timestamp}'

    class Meta:
        ordering = ['timestamp']
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
