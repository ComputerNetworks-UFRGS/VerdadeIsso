
from django import forms
from .models import UploadedFile, UploadedText
from django.db import models

class UploadFileForm(forms.ModelForm):
    arquivo = forms.FileField(label='Arquivo')
    class Meta:
        model = UploadedFile
        fields = ['arquivo']
       
class UploadTextForm(forms.ModelForm):
    texto = models.TextField()
    class Meta:
        model = UploadedText
        fields = ['texto']
