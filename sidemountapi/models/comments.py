from django.db import models

class Comment(models.Model):
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    author = models.ForeignKey("SideMountUser", on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=250)
    created_on = models.DateField(null=False, blank=False, auto_now=False, auto_now_add=True)