from django.db import models
from django.contrib.auth.models import User

class SideMountUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=155)
    profile_image_url = models.TextField(null=True, blank=True)
    belt = models.ForeignKey('Belt', on_delete=models.CASCADE)
