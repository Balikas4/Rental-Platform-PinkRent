from django.contrib import admin
from . import models
from .forms import FeedbackForm
from modeltranslation.admin import TranslationAdmin


class ListingAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'owner', 'is_available', 'price', 'brand', 'category']
    list_editable = ['is_available', 'category']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'parent']

class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('id', 'name',)

class TagAdmin(TranslationAdmin):
    list_display = ('id', 'name',)
    search_fields = ('id', 'name',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'listing', 'rate', 'created_at']
    list_editable = ['rate']

class WaitlistEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'created_at')
    search_fields = ('email',)

class FeedbackAdmin(admin.ModelAdmin):
    form = FeedbackForm  # Link the form to the admin
    list_display = ['id', 'comment', 'rating']  # Adjust fields as necessary
    search_fields = ['comment', 'rating', 'id']

admin.site.register(models.ListingReview, ReviewAdmin)
admin.site.register(models.Listing, ListingAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Brand, BrandAdmin)
admin.site.register(models.WaitlistEntry, WaitlistEntryAdmin)
admin.site.register(models.Feedback, FeedbackAdmin)