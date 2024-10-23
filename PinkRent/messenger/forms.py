# messenger/forms.py
from django import forms
from .models import Message  # Adjust the import based on your project structure

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message  # The model you want to create or update
        fields = ['content']  # Include the fields you want to show in the form
