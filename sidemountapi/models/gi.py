from django.db import models

class Gi(models.Model):
    label = models.CharField(max_length=100)