from django.shortcuts import render, redirect
from .forms import UploadFileForm, UploadTextForm, CheckFileForm
import hashlib
from .models import UploadedFile, UploadedText, CheckedFile, Sources
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')


def check_file(request):
    if request.method == 'POST':
        form = CheckFileForm(request.POST, request.FILES)
        #form2 = UploadTextForm(request.POST)
        if form.is_valid():
            uploaded_file = form.cleaned_data
            # Read the content of the uploaded file
            content = uploaded_file['arquivo'].read().decode('utf-8')
            # Calculate the hash of the content
            file_hash = hashlib.sha256(content.encode()).hexdigest()
            exists = UploadedFile.objects.filter(hash_value=file_hash).exists()
            if exists:
               uploaded_file = form.save(commit=False) 
               uploaded_file.fake = True # Fakenews flag
               uploaded_file.save()
               fakenews = UploadedFile.objects.get(hash_value=file_hash)
               fakenews_sources = fakenews.Fontes.all()
               content = list(fakenews_sources.values()) 
               return render(request, 'fake.html', {'content': content, 'file_hash': file_hash})
            else: # Aqui implementamos algo em caso da hash não existir
               uploaded_file = form.save() # Salva como checked file, mas não como fakenews
               # Aqui a gente implementa algo em caso de hash não existir.
               return render(request, 'sem-hash.html', {'content': content, 'file_hash': file_hash})
    else:
        form = CheckFileForm()
        #form2 = UploadTextForm()
    return render(request, 'check.html', {'form': form})


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        #form2 = UploadTextForm(request.POST)
        if form.is_valid():
            uploaded_file = form.cleaned_data
            # Read the content of the uploaded file
            content = uploaded_file['arquivo'].read().decode('utf-8')
            # Calculate the hash of the content
            file_hash = hashlib.sha256(content.encode()).hexdigest()
            exists = UploadedFile.objects.filter(hash_value=file_hash).exists()
            if exists:
               return render(request, 'existe.html', {'content': content, 'file_hash': file_hash})
            else:
               uploaded_file = form.save()
               return render(request, 'upload_success.html', {'content': content, 'file_hash': file_hash})
    else:
        form = UploadFileForm()
        form2 = UploadTextForm()
    return render(request, 'upload.html', {'form': form, 'form2': form2})
    
def data_dump(request):
    fatos = Sources.objects.all()
    content = list(fatos.values())
    return render(request, 'data_dump.html', {'content': content})

