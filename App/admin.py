from django.contrib import admin
from .models import UploadedFile, CheckedFile, Sources, UploadedText # Import your models

# Register your models here.
admin.site.register(UploadedFile)
admin.site.register(CheckedFile)
admin.site.register(Sources)
admin.site.register(UploadedText)

