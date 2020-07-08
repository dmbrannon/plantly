from django import forms
from .models import Entry

class EntryCreateForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['plant', 'note', 'watered', 'fertilized', 'repotted', 'treated']
        widgets = {
            'plant': forms.HiddenInput,
        }