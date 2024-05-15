
from django import forms
from .models import UploadedFile, UploadedText, CheckedFile, Sources
from django.db import models

class UploadFileForm(forms.ModelForm):
    arquivo = forms.FileField(label='Arquivo')
    Fontes = models.ManyToManyField(Sources)
    class Meta:
        model = UploadedFile
        fields = ['arquivo', 'Fontes']
       
class UploadTextForm(forms.ModelForm):
    texto = models.TextField()
    class Meta:
        model = UploadedText
        fields = ['texto']

class CheckFileForm(forms.ModelForm):
    arquivo = forms.FileField(label='Arquivo')
    fake = models.BooleanField(default=False)
    class Meta:
        model = CheckedFile
        fields = ['arquivo']
