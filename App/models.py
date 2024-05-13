from django.db import models
import hashlib

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    hash_value = models.CharField(max_length=64, blank=True)

    def save(self, *args, **kwargs):
        if not self.hash_value:
            # Calculate the hash of the file content
            hash_object = hashlib.sha256()
            for chunk in self.file.chunks():
                hash_object.update(chunk)
            self.hash_value = hash_object.hexdigest()
        super().save(*args, **kwargs)
