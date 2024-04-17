from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['category', 'picture', 'name', 'brand', 'size', 'quality', 'color', 'value', 'price', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can customize form widgets or add additional settings here if needed
