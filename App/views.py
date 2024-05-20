from django.shortcuts import render, redirect
from .forms import UploadFileForm, UploadTextForm, CheckFileForm, CheckTextForm, addSourceForm
import hashlib
from .models import UploadedFile, UploadedText, CheckedText, CheckedFile, Sources
from django.http import JsonResponse
from accounts.models import User
from accounts.forms import UserCreationForm, Autenticacao
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .text_check import get_similar_text
from .image_check import check_image_api
from itertools import chain


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('upload_file')
    
    def form_invalid(self, form):
        messages.error(self.request,'Erro: Nome de usuário incorreto ou senha inválida')
        return self.render_to_response(self.get_context_data(form=form))



def check_file(request):
    if request.method == 'POST':
        form = CheckFileForm(request.POST, request.FILES)
        form2 = CheckTextForm(request.POST)
        if form.is_valid():
            uploaded_file = form.cleaned_data
            # Read the content of the uploaded file
            content = uploaded_file['arquivo'].read()
            # Calculate the hash of the content
            file_hash = hashlib.sha256(content).hexdigest()
            exists = UploadedFile.objects.filter(hash_value=file_hash).exists()
            if exists:
                uploaded_file = form.save(commit=False) 
                uploaded_file.fake = True # Fakenews flag
                uploaded_file.save()
                fakenews = UploadedFile.objects.get(hash_value=file_hash)
                fakenews_sources = fakenews.Fontes.all()
                content = list(fakenews_sources.values())
                return render(request, 'fake.html', {'content': content, 'file_hash': file_hash})
            else:
                output = check_image_api(content)
                if output['ai_generated'] > 0.5:
                    return render(request, 'ai-generated.html', {'content': float(output['ai_generated']) * 100})
                else:
                    return render(request, 'sem-hash.html', {'content': content, 'file_hash': file_hash})
        if form2.is_valid(): # If text
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
                print(content)
                return render(request, 'fake.html', {'content': content, 'file_hash': text_hash})
            else:
                docs = get_similar_text(content)
                if docs:
                    unique_content = set(tuple(d.items()) for d in chain.from_iterable(d.Fontes.all().values() for d in docs))
                    content = [dict(item) for item in unique_content]
                    print(content)
                    return render(request, 'similar.html', {'content': content})
                else:
                    uploaded_text = form2.save()
                    return render(request, 'sem-hash.html', {'content': content, 'file_hash': text_hash})
    else:
        form = CheckFileForm()
        form2 = CheckTextForm()
    return render(request, 'check.html', {'form': form, 'form2': form2})

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        form2 = UploadTextForm(request.POST)
        if form.is_valid(): # If file
            uploaded_file = form.cleaned_data
            # Read the content of the uploaded file
            content = uploaded_file['arquivo'].read()
            # Calculate the hash of the content
            file_hash = hashlib.sha256(content).hexdigest()
            exists = UploadedFile.objects.filter(hash_value=file_hash).exists()
            if exists:
               fakenews = UploadedFile.objects.get(hash_value=file_hash)
               fakenews_sources = fakenews.Fontes.all()
               content = list(fakenews_sources.values()) 
               return render(request, 'existe.html', {'content': content, 'file_hash': file_hash})
            else:
               uploaded_file = form.save()
               return render(request, 'upload_success.html', {'content': content, 'file_hash': file_hash})
        if form2.is_valid(): # If text
            content = form2.cleaned_data
            texto = content['texto']
            text_hash = hashlib.sha256(texto.encode()).hexdigest()
            exists = UploadedText.objects.filter(hash_value=text_hash).exists()
            if exists:
              fakenews = UploadedText.objects.get(hash_value=text_hash)
              fakenews_sources = fakenews.Fontes.all()
              content = list(fakenews_sources.values())
              return render(request, 'existe.html', {'content': content, 'file_hash': text_hash})
            else:
               content = form2.save()
               return render(request, 'upload_success.html', {'content': texto, 'file_hash': text_hash})
    else:
        form = UploadFileForm() # Form is to upload files
        form2 = UploadTextForm() # Form2 is to upload text
    return render(request, 'upload.html', {'form': form, 'form2': form2})

@login_required
def add_source(request):
   print(request.method)
   if request.method == 'POST':
      form = addSourceForm(request.POST)
      if form.is_valid():
         addSource = form.save()
         uploadfile = UploadFileForm()
         uploadtext = UploadTextForm()
         return render(request, 'upload.html', {'form': uploadfile, 'form2': uploadtext}) # Send the updated forms to load the /upload/ again
   else:
      form = addSourceForm()
      return render(request, 'add_source.html', {'form': form})
    
def data_dump(request):
    fatos = Sources.objects.all()
    content = list(fatos.values())
    fake = UploadedText.objects.all() # Return all fakenews already uploaded
    fake_text = list(fake.values())

   #init contagem de exemplos
    fontes = []
    fake_text = list(UploadedText.objects.values('Fontes'))	 # Get all texts uploaded and its sources association
    for fato in content:
        count=0
        for fake in fake_text:
            if fake['Fontes'] == fato['id']:
                count+=1 
        fontes.append(count)
    content2=[]
    i=0
    for item in content:
        item.update({'countExemplos':fontes[i]})
        i+=1
    # end contagem exemplos


    return render(request, 'data_dump.html', {'content': content, 'fake': fake_text})

def fake_samples(request, value_id):
    fonte_title = Sources.objects.get(id=value_id) # Return the title of a source the specific ID
    fake_text = UploadedText.objects.prefetch_related('Fontes') # Get all texts uploaded and its sources association
    for text in fake_text:
        fontes = text.Fontes.all()
    return render(request, 'fake_samples.html', {'fake_text': fake_text, 'fontes': fontes, 'value_id': value_id, 'fonte_title': fonte_title})
    
def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def index(request):
    fatos = Sources.objects.all()
    content = list(fatos.values())
    totalFatos = len(content)

   #init contagem de exemplos
    fontes = []
    fake_text = list(UploadedText.objects.values('Fontes'))	 # Get all texts uploaded and its sources association
    for fato in content:
        count=0
        for fake in fake_text:
            if fake['Fontes'] == fato['id']:
                count+=1 
        fontes.append(count)
    content2=[]
    i=0
    for item in content:
        item.update({'countExemplos':fontes[i]})
        i+=1
    # end contagem exemplos

    totalCheckedFiles = CheckedFile.objects.all().count()
    totalCheckedText = CheckedText.objects.all().count()
    totalChecked = totalCheckedFiles + totalCheckedText    

    totalFakeFiles = CheckedFile.objects.all().filter(fake='True').count()
    totalFakeText = CheckedText.objects.all().filter(fake='True').count()
    totalFake = totalFakeFiles + totalFakeText

    totalMapeamentos = UploadedFile.objects.values('Fontes').count()
    totalMapeamentos += UploadedText.objects.values('Fontes').count()
   
    return render(request, 'index.html', {'fake_text':fontes, 'content': content[:5], 'totalFake': totalFake, 'totalFontes': totalFatos, 'totalChecked': totalChecked, 'totalMapeamentos': totalMapeamentos})
