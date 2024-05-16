from django.shortcuts import render, redirect
from .forms import UploadFileForm, UploadTextForm, CheckFileForm, CheckTextForm
import hashlib
from .models import UploadedFile, UploadedText, CheckedFile, Sources
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')


def check_file(request):
    if request.method == 'POST':
        form = CheckFileForm(request.POST, request.FILES)
        form2 = CheckTextForm(request.POST)
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
        if form2.is_valid():
           uploaded_text = form2.cleaned_data
           content = uploaded_text['texto']
           text_hash = hashlib.sha256(content.encode()).hexdigest()
           exists = UploadedText.objects.filter(hash_value=text_hash).exists()
           if exists:
              content = form2.save(commit=False)
              content.fake = True
              content.save()
              fakenews = UploadedText.objects.get(hash_value=text_hash)
              fakenews_sources = fakenews.Fontes.all()
              content = list(fakenews_sources.values())
              return render(request, 'fake.html', {'content': content, 'file_hash': text_hash})
           else:
              uploaded_text = form2.save()
              return render(request, 'sem-hash.html', {'content': content, 'file_hash': text_hash})
    else:
        form = CheckFileForm()
        form2 = CheckTextForm()
    return render(request, 'check.html', {'form': form, 'form2': form2})


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        form2 = UploadTextForm(request.POST)
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
        if form2.is_valid():
            content = form2.cleaned_data
            texto = content['texto']
            text_hash = hashlib.sha256(texto.encode()).hexdigest()
            exists = UploadedText.objects.filter(hash_value=text_hash).exists()
            if exists:
               return render(request, 'existe.html', {'content': content, 'file_hash': text_hash})
            else:
               content = form2.save()
               return render(request, 'upload_success.html', {'content': texto, 'file_hash': text_hash})
    else:
        form = UploadFileForm() # Form é o upload de arquivos
        form2 = UploadTextForm() # Form2 é o upload de texto
    return render(request, 'upload.html', {'form': form, 'form2': form2})
    
def data_dump(request):
    fatos = Sources.objects.all()
    content = list(fatos.values())
    return render(request, 'data_dump.html', {'content': content})

def home_page(request):
    return render(request, 'index.html')

