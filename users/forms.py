from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.template.defaultfilters import filesizeformat
from django.conf import settings
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['image'].help_text = "The maxmiumum file size is 5 MB"
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
        model = Profile
        fields = ['image']