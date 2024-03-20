from django.contrib import admin
from . import models


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'picture']
    list_editable = ['picture']


admin.site.register(models.UserProfile, UserProfileAdmin)
