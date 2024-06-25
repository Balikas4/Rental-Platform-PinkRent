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
        super(ListingForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            category = self.instance.category
            if category and category.parent:
                self.fields['category'].queryset = category.parent.subcategories.all()
            else:
                self.fields['category'].queryset = Category.objects.all()
        else:
            self.fields['category'].queryset = Category.objects.all()

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
