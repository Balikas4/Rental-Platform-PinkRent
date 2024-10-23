from django.conf import settings
from messenger.models import Message


def google_analytics(request):
    return {
        'GOOGLE_ANALYTICS_ID': getattr(settings, 'GOOGLE_ANALYTICS_ID', None),
    }

def unread_messages_count(request):
    if request.user.is_authenticated:
        # Get the count of unread messages where the user is the receiver
        unread_count = Message.objects.filter(receiver=request.user, read=False).count()
    else:
        unread_count = 0

    return {
        'unread_count': unread_count,
    }