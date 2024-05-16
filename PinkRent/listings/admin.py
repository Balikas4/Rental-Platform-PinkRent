from django.contrib import admin
from . import models


class ListingAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'owner', 'is_available', 'price', 'brand', 'category']
    list_editable = ['is_available', 'category']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'listing', 'rate', 'created_at']
    list_editable = ['rate']

admin.site.register(models.ListingReview, ReviewAdmin)
admin.site.register(models.Listing, ListingAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Tag, TagAdmin)