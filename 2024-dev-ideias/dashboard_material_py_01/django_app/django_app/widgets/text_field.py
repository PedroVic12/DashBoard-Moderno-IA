# django_app/forms.py

from django import forms
from .models import ImageUpload


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ["image"]


# django_app/forms.py

from django import forms
from .models import ImageUpload


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ["image"]
