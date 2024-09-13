# scraper/models.py
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    date = models.DateField()
    origin = models.CharField(max_length=255)
    url = models.URLField()

    category = models.CharField(max_length=255, blank=True, null=True)  # Add this field if needed

    def __str__(self):
        return self.title
