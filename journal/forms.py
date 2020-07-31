from django import forms
from django.forms.widgets import FileInput
from django.template.defaultfilters import filesizeformat
from django.conf import settings
from image_cropping import ImageCropWidget
from .models import Entry, Plant

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
        self.fields['image'].help_text = "Max file size: 5 MB<br> WARNING: This image will be cropped to a square"

    def clean_image(self):
        image = self.cleaned_data['image']
        try:
            content_type = image.content_type.split('/')[0]
            if content_type in settings.CONTENT_TYPES:
                if image.size > int(settings.MAX_UPLOAD_SIZE):
                    raise forms.ValidationError(('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(image.size)))
            else:
                raise forms.ValidationError('File type is not supported')
            return image
        except:
            return image

    class Meta:
        model = Plant
        fields = ['name', 'location', 'bought', 'schedule', 'image', 'cropping']
        widgets = {
            'bought': forms.SelectDateWidget,
            'image': FileInput,
        }
