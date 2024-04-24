from django.contrib import admin
from . import models
from listings.models import Listing


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'picture']
    list_editable = ['picture']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'rate', 'created_at', 'profile']
    list_editable = ['rate']
    list_display_links = ['profile', 'user', 'id']

admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.UserProfileReview, ReviewAdmin)  # Register Review model with ReviewAdmin
