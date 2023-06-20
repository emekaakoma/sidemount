from django.db import models
from django.contrib.auth.models import User

class SideMountUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=155)
    belt = models.ForeignKey('Belt', on_delete=models.CASCADE)
