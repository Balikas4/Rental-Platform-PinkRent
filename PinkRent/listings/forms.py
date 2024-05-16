from django import forms
from .models import Listing, ListingReview, Tag

class ListingForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Listing
        fields = ['category', 'picture', 'name', 'brand', 'size', 'quality', 'color', 'value', 'price', 'description', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can customize form widgets or add additional settings here if needed

class ListingReviewForm(forms.ModelForm):
    class Meta:
        model = ListingReview
        fields = ['comment', 'rate']
        labels = {
            'comment': 'Comment',
            'rate': 'Rating',
        }
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            'rate': forms.NumberInput(attrs={'min': 0, 'max': 5}),
        }