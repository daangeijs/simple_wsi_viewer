# models.py

from django.db import models

class Image(models.Model):
    name = models.CharField(max_length=255)
    path = models.FilePathField()  # store the relative path to the image
    thumbnail = models.FilePathField(null=True, blank=True)

class IndexingStatus(models.Model):
    finished = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True)