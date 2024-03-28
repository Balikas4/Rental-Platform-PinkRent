from django.db import models
from django.contrib.auth import get_user_model
from listings.models import Listing
from django.utils import timezone

class Offer(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sent_offers')
    receiver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='received_offers')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    duration_days = models.IntegerField()
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Offer from {self.sender.username} to {self.receiver.username} for {self.listing.name}"
