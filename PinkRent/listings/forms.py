from django import forms
from .models import Listing, ListingReview, Tag, Category, Brand, Feedback

class ListingForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(parent=None),
        required=True,
        label="Category"
    )

    size = forms.ChoiceField(
        choices=Listing.SIZE_CHOICES,
        required=True,
        label="Size"
    )

    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(), 
        required=False, 
        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Listing
        fields = ['category', 'picture', 'picture_1', 'picture_2', 'picture_3', 'name', 'brand', 'size', 'quality', 'color', 'value', 'price', 'is_for_sale', 'description', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['category'].queryset = Category.objects.filter(id=category_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Category queryset
        elif self.instance.pk and self.instance.category:
            self.fields['category'].queryset = self.instance.category.parent.subcategories.all()

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

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comment', 'rating']
