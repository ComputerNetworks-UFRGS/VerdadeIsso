# -*- coding: utf-8 -*-
# !/usr/bin/env python

from App.models import *
from django.contrib.auth.models import Group
from accounts.models import User
import requests
import os

import requests

def search_facts(query, api_key):
    api_url = 'https://factchecktools.googleapis.com/v1alpha1/claims:search'

    params = {
        'query': query,
        'maxAgeDays': 15,  # Limit results to those published within the last 7 days
        'pageSize': 1000,    # Limit number of results to 5
        'key': api_key    # Include your API key here
    }

    response = requests.get(api_url, params=params)
    i=0
    if response.status_code == 200:
        data = response.json()
        for claim in data.get('claims', []):
            i = i+1
            fakenews = Sources(title=claim['text'], link=claim['claimReview'][0]['url'], web_source=claim['claimReview'][0]['publisher']['name'])
            fakenews.save()

    else:
        print('Failed to retrieve data. Status code:', response.status_code)
    print(i)

# Inicio do Populator

# Database eraser
Sources.objects.all().delete()
UploadedFile.objects.all().delete()
UploadedText.objects.all().delete()
CheckedFile.objects.all().delete()
CheckedText.objects.all().delete()

# Add sources from websites
#search_facts(['RS', 'Rio Grande do Sul', 'Enchentes'], 'API') # Change API for Google API Key

# Database eraser
#Sources.objects.all().delete()
UploadedFile.objects.all().delete()
UploadedText.objects.all().delete()
CheckedFile.objects.all().delete()
CheckedText.objects.all().delete()

textosfake = UploadedText.objects.create(texto = "O RS está procurando duas gaúchas…, precisam da ajuda delas! É uma tal de XUXA e outra se chama MANUELA DÁVILA (essa, até o padre está procurando, porque ela não voltou na missa") # Adiciona o conteúdo fake
textosfake.save()
fonte, _ = Sources.objects.get_or_create(id=64) # Add id of the fakenews source
textosfake.Fontes.add(fonte)
textosfake.save()

with open('video.mp4', 'rb') as file:
   arquivosfake = UploadedFile.objects.create(arquivo="video.mp4")
   arquivosfake.save()
fonte, _ = Sources.objects.get_or_create(id=66) # Add id of the fakenews source
arquivosfake.Fontes.add(fonte)
arquivosfake.save()


