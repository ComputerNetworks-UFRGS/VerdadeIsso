from django.db import models
import hashlib

class UploadedFile(models.Model):
    arquivo = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    hash_value = models.CharField(max_length=64, blank=True)

    def save(self, *args, **kwargs):
        if not self.hash_value:
            # Calculate the hash of the file content
            hash_object = hashlib.sha256()
            for chunk in self.arquivo.chunks():
                hash_object.update(chunk)
            self.hash_value = hash_object.hexdigest()
        super().save(*args, **kwargs)

class CheckedFile(models.Model):
    arquivo = models.FileField(upload_to='uploads/')
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

class UploadedText(models.Model):
    texto = models.TextField(max_length=1000)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    hash_value = models.CharField(max_length=64, blank=True)

    #def save(self, *args, **kwargs):
        #if not self.hash_value:
            # Calculate the hash of the file content
            #hash_object = hashlib.sha256()
            #for chunk in self.arquivo.chunks():
             #   hash_object.update(chunk)
            #self.hash_value = hash_object.hexdigest()
        #super().save(*args, **kwargs)
