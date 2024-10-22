from django import forms
from .models import Listing, ListingReview, Tag, Category, Brand, Feedback

class ListingForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        required=False,
        label="Occasion"
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
        fields = ['category', 'picture', 'picture_1', 'picture_2', 'picture_3', 'name', 'brand', 'size', 'quality', 'color', 'value', 'price', 'is_for_sale', 'sell_price', 'description', 'tags']

    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)

        # Add a blank choice to tags
        self.fields['tags'].widget.choices = [('')] + list(self.fields['tags'].widget.choices)

        # Update queryset for category based on instance
        if self.instance and self.instance.pk:
            category = self.instance.category
            if category and category.parent:
                self.fields['category'].queryset = category.parent.subcategories.all()
            else:
                self.fields['category'].queryset = Category.objects.all()
        else:
            self.fields['category'].queryset = Category.objects.all()

        # Set dynamic quality and color choices based on the instance's language
        if self.instance:
            self.fields['quality'].choices = self.instance.get_quality_choices()
            self.fields['color'].choices = self.instance.get_color_choices()
        else:
            # Default to the choices based on the current language
            self.fields['quality'].choices = Listing().get_quality_choices()
            self.fields['color'].choices = Listing().get_color_choices()


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

class JoinWaitlistForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email',
        'class': 'waitlist-email-input'
    }))
