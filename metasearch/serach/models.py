from django.db import models

class URLdata(models.Model):
    url = models.CharField(max_length=255)
    rank = models.FloatField(default=0)
    title = models.CharField(default="",max_length=255)
    se = models.CharField(default="",max_length=255)
