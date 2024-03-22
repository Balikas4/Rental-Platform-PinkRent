from django.contrib import admin
from . import models


class ListingAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'owner', 'is_available', 'price', 'brand', 'category']
    list_editable = ['is_available', 'category']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(models.Listing, ListingAdmin)
admin.site.register(models.Category, CategoryAdmin)