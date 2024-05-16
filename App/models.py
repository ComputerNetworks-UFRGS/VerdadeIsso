from django.db import models
import hashlib

class Sources(models.Model):
    title = models.CharField(max_length=100, blank=True)
    link = models.CharField(max_length=64, blank=True)
    web_source = models.CharField(max_length=64, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return self.title
           
class UploadedFile(models.Model):
    arquivo = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    hash_value = models.CharField(max_length=64, blank=True)
    Fontes = models.ManyToManyField(Sources)

    def save(self, *args, **kwargs):
        if not self.hash_value:
            # Calculate the hash of the file content
            hash_object = hashlib.sha256()
            for chunk in self.arquivo.chunks():
                hash_object.update(chunk)
            self.hash_value = hash_object.hexdigest()
        super().save(*args, **kwargs)
    def __str__(self):
       return self.hash_value

class CheckedFile(models.Model):
    arquivo = models.FileField(upload_to='uploads/', blank=True)
    hash_value = models.CharField(max_length=64, blank=True)
    fake = models.BooleanField(default=False)
    checked_at = models.DateTimeField(auto_now_add=True)

    def save(self, fake=None, *args, **kwargs):
        if not self.hash_value:
        # Calculate the hash of the file content
            hash_object = hashlib.sha256()
            for chunk in self.arquivo.chunks():
                hash_object.update(chunk)
            self.hash_value = hash_object.hexdigest()
        if fake is not None:
            self.fake = fake
        super().save(*args, **kwargs)
        
    def __str__(self):
       return self.hash_value
       
class UploadedText(models.Model):
    texto = models.TextField(max_length=1000, default="Insira o texto que deseja verificar.")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    hash_value = models.CharField(max_length=64, blank=True)
    Fontes = models.ManyToManyField(Sources)

    def save(self, *args, **kwargs):
        if not self.hash_value:
            # Calculate the hash of the text content
            hash_object = hashlib.sha256()
            self.hash_value = hash_object.hexdigest()
        super().save(*args, **kwargs)
    
    def __str__(self):
       return self.hash_value
