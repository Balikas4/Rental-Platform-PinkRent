from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['name', 'picture', 'price', 'brand', 'description', 'is_available']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can customize form widgets or add additional settings here if needed
