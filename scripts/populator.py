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

noticias = ["Se deixar, o prefeito de CANOAS muda o nome da cidade para HAVANA DO SUL. Jairo Jorge, do PSD, baixou um decreto para tomar bens particulares e distribuir à população. Tudo fica pior ao saber que somente a prefeitura quer aparecer na foto. Toda a distribuição está centralizada nas mãos do prefeito e seus capangas, que não deixa ninguém mais entregar os mantimentos necessários. Entenda: a prefeitura quer ser A ÚNICA a distribuir as doações que chegam do Brasil inteiro, e até do exterior. Em troca, ela exige um cadastro de quem recebe. Qual o objetivo do patife? Votos, apenas votos. Jairo Jorge está explorando o desespero da população pensando nas eleições. Veja o decreto.", "tá sabendo da denúncia da edição de um decreto que o Jairo Jorge fez, dando poder pra prefeitura confiscar doações privadas???? “Requisição administrativa de bens privados”", "URGENTE – Segundo esta denúncia, a prefeitura de Canoas está monopolizando as doações e mentindo para a população Estão afirmando que as cestas básicas foram compradas pela prefeitura quando na verdade trata-se de doações voluntárias.", "URGENTE – Segundo esta denúncia, a prefeitura de Canoas está monopolizando as doações e mentindo para a população", "Absurdo dos absurdos, prefeito de Canoas emite um decreto o de confisca as doações, isso é um absurdo do tamanho do mundo, ele não pode confiscar bens de outros isso é ditadura.", "Através de decreto, o prefeito de Canoas, confisca as doações, os PETRALHAS não param!!! Lembrando, é amiguinho do MONTANHA!!!", "PREFEITO DE CANOAS ( PT ), EDITOU DECRETO DE APROPRIAÇÃO DE DONATIVOS. E ESTÁ REEMBALANDO COM SELO DO GOVERNO FEDERAL. PT É UMA ORGANIZAÇÃO CRIMINOSA DE FILHOS DE PUTA !"]
for i in noticias:
   textosfake = UploadedText.objects.create(texto=i) # Adiciona o conteúdo fake
   textosfake.save()
   fonte, _ = Sources.objects.get_or_create(id=112) # Add id of the fakenews source
   textosfake.Fontes.add(fonte)
   textosfake.save()

with open('video.mp4', 'rb') as file:
   arquivosfake = UploadedFile.objects.create(arquivo="video.mp4")
   arquivosfake.save()
fonte, _ = Sources.objects.get_or_create(id=66) # Add id of the fakenews source
arquivosfake.Fontes.add(fonte)
arquivosfake.save()


