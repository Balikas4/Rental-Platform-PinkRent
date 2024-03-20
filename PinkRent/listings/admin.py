from django.contrib import admin
from . import models


class ListingAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'owner', 'is_available', 'price', 'brand']
    list_editable = ['is_available']


admin.site.register(models.Listing, ListingAdmin)
