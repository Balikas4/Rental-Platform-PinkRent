# offers/forms.py
from django import forms
from django.contrib.auth import get_user_model
from .models import Offer, Listing

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['receiver', 'listing', 'message', 'duration_days', 'start_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, user, listing, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)

        # Set the receiver field to the owner of the listing
        self.fields['receiver'].initial = listing.owner
        self.fields['receiver'].widget = forms.HiddenInput()

        self.fields['listing'].initial = listing
        self.fields['listing'].widget = forms.HiddenInput()  # Hide the listing field in the form

        # Exclude the current user from the receiver queryset (if necessary)
        # self.fields['receiver'].queryset = get_user_model().objects.exclude(id=user.id)
