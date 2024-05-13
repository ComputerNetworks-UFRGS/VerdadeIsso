from django.shortcuts import render, redirect
from .forms import UploadFileForm
import hashlib
from .models import UploadedFile
from django.http import JsonResponse

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            # Read the content of the uploaded file
            content = uploaded_file.file.read().decode('utf-8')
            # Calculate the hash of the content
            file_hash = hashlib.sha256(content.encode()).hexdigest()
            exists = UploadedFile.objects.filter(hash_value=file_hash).exists()
            if exists:
               return render(request, 'fake.html', {'content': content, 'file_hash': file_hash})
            else:
               return render(request, 'upload_success.html', {'content': content, 'file_hash': file_hash})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
