from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from django.forms import ModelForm
from django import forms
import os

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields =('username','email','password1','password2')


class VideoUploadForm(forms.Form):
    video_file = forms.FileField(label="Upload your video")
    language_code = forms.ChoiceField(
        choices=[
            ('en', 'English'),
            ('hi', 'Hindi'),
            ('te', 'Telugu'),
            ('ta', 'Tamil'),
            ('ml', 'Malayalam'),
            ('kn', 'Kannada'),
            ('bn', 'Bengali'),
            ('gu', 'Gujarati'),
            ('mr', 'Marathi'),
            ('pa', 'Punjabi'),
            ('ur', 'Urdu'),
            ('fr', 'French'),
            ('es', 'Spanish'),
            ('de', 'German'),
            ('ru', 'Russian'),
            ('zh-CN', 'Chinese (Simplified)'),
            ('ja', 'Japanese'),
            ('ar', 'Arabic'),
        ],
        label="Translate to"
    )



    def clean_video_file(self):
        file = self.cleaned_data.get('video_file')
        if file:
            # Validate MIME type
            if not file.content_type.startswith('video/'):
                raise forms.ValidationError("The uploaded file is not a valid video format.")

            # Optionally check file extension too
            ext = os.path.splitext(file.name)[1].lower()
            allowed_exts = ['.mp4', '.avi', '.mov', '.mkv']
            if ext not in allowed_exts:
                raise forms.ValidationError("Only video files (.mp4, .avi, .mov, .mkv) are supported.")
        return file
