from django.db import models

class Belt(models.Model):
    label = models.CharField(max_length=100)