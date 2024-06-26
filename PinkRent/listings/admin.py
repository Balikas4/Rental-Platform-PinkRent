from django.contrib import admin
from . import models


class ListingAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'owner', 'is_available', 'price', 'brand', 'category']
    list_editable = ['is_available', 'category']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']

class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('id', 'name',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('id', 'name',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'listing', 'rate', 'created_at']
    list_editable = ['rate']

class WaitlistEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'created_at')
    search_fields = ('email',)

admin.site.register(models.ListingReview, ReviewAdmin)
admin.site.register(models.Listing, ListingAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Brand, BrandAdmin)
admin.site.register(models.WaitlistEntry, WaitlistEntryAdmin)