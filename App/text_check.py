""" Verifica texto com textos parecidos no banco de dados """
from difflib import SequenceMatcher
from .models import UploadedText

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def get_similar_text(query_text, threshold=0.5):
    # Fetch all documents
    all_documents = UploadedText.objects.all()

    # Filter documents based on similarity
    similar_documents = [
        doc for doc in all_documents
        if similar(query_text, doc.texto) >= threshold
    ]
    return similar_documents
