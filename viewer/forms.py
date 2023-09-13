from django import forms
from .models import TiffFile

class TiffFileForm(forms.ModelForm):
    class Meta:
        model = TiffFile
        fields = ('uploaded_file',)