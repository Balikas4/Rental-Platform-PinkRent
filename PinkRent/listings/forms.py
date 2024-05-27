from django import forms
from .models import Listing, ListingReview, Tag, Category

class ListingForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    parent_category = forms.ModelChoiceField(
        queryset=Category.objects.filter(parent=None),
        required=True,
        label="Parent Category"
    )

    sub_category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        required=True,
        label="Sub Category"
    )

    size = forms.ChoiceField(
        choices=Listing.SIZE_CHOICES,
        required=True,
        label="Size"
    )

    class Meta:
        model = Listing
        fields = ['parent_category', 'sub_category', 'picture', 'name', 'brand', 'size', 'quality', 'color', 'value', 'price', 'description', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'parent_category' in self.data:
            try:
                parent_id = int(self.data.get('parent_category'))
                self.fields['sub_category'].queryset = Category.objects.filter(parent_id=parent_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty SubCategory queryset
        elif self.instance.pk and self.instance.sub_category:
            self.fields['sub_category'].queryset = self.instance.sub_category.parent.subcategory_set.all()

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