from django import forms
from .models import Entry, Plant
from image_cropping import ImageCropWidget

class EntryCreateForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['plant', 'note', 'watered', 'fertilized', 'repotted', 'treated']
        widgets = {
            'plant': forms.HiddenInput,
        }

class EntryWaterForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['watered']
        widgets = {
            'watered': forms.HiddenInput,
        }

class PlantCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PlantCreateForm, self).__init__(*args, **kwargs)
        self.fields['schedule'].help_text = "Enter the number of days between waterings <i>(e.g.  7)</i>"
        self.fields['location'].help_text = "<i>(e.g.  Kitchen)</i>"
        self.fields['image'].help_text = "WARNING: This image will be cropped to a square"

    class Meta:
        model = Plant
        fields = ['name', 'location', 'bought', 'schedule', 'image', 'cropping']
        widgets = {
            'bought': forms.SelectDateWidget,
            'image': ImageCropWidget,
        }
