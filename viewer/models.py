from django.db import models

class UploadedFile(models.Model):
    uploaded_file = models.FileField(upload_to='uploads/')
    dzi_file = models.FilePathField(blank=True, null=True)