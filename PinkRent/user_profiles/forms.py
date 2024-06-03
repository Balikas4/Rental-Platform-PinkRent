from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from . import models
from .models import UserProfileReview
from django.utils.translation import gettext as _

class CreateUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['username'].help_text = ''


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", )


class UserProfileForm(forms.ModelForm):
    show_instagram = forms.BooleanField(required=False, label=_("Show Instagram"))
    instagram_url = forms.URLField(required=False, label=_("Instagram URL"))

    show_facebook = forms.BooleanField(required=False, label=_("Show Facebook"))
    facebook_url = forms.URLField(required=False, label=_("Facebook URL"))

    show_phone = forms.BooleanField(required=False, label=_("Show Phone Number"))
    phone_number = forms.CharField(required=False, label=_("Phone Number"))

    show_email = forms.BooleanField(required=False, label=_("Show Email"))
    email = forms.EmailField(required=False, label=_("Email"))

    class Meta:
        model = models.UserProfile
        fields = ('picture', 'city', 'show_instagram', 'instagram_url', 'show_facebook', 'facebook_url', 'show_phone', 'phone_number', 'show_email', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.contact_options:
            contact_options = self.instance.contact_options
            self.fields['show_instagram'].initial = 'IG' in contact_options
            self.fields['instagram_url'].initial = contact_options.get('IG', '')
            self.fields['show_facebook'].initial = 'FB' in contact_options
            self.fields['facebook_url'].initial = contact_options.get('FB', '')
            self.fields['show_phone'].initial = 'NUM' in contact_options
            self.fields['phone_number'].initial = contact_options.get('NUM', '')
            self.fields['show_email'].initial = 'EMAIL' in contact_options
            self.fields['email'].initial = contact_options.get('EMAIL', '')

    def save(self, commit=True):
        instance = super().save(commit=False)
        contact_options = {}
        if self.cleaned_data.get('show_instagram'):
            contact_options['IG'] = self.cleaned_data.get('instagram_url', '')
        if self.cleaned_data.get('show_facebook'):
            contact_options['FB'] = self.cleaned_data.get('facebook_url', '')
        if self.cleaned_data.get('show_phone'):
            contact_options['NUM'] = self.cleaned_data.get('phone_number', '')
        if self.cleaned_data.get('show_email'):
            contact_options['EMAIL'] = self.cleaned_data.get('email', '')
        instance.contact_options = contact_options
        if commit:
            instance.save()
        return instance


class ProfileReviewForm(forms.ModelForm):
    class Meta:
        model = UserProfileReview
        fields = ['comment', 'rate']
        labels = {
            'comment': 'Comment',
            'rate': 'Rating',
        }
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            'rate': forms.NumberInput(attrs={'min': 0, 'max': 5}),
        }