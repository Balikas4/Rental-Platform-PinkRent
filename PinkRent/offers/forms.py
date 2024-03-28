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

    def __init__(self, user, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)

        self.fields['receiver'].queryset = get_user_model().objects.exclude(id=user.id)

        self.fields['listing'].queryset = Listing.objects.all()

