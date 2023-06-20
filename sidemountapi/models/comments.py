from django.db import models

class Comment(models.Model):
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    author = models.ForeignKey("SideMountUser", on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=250)
    created_on = models.DateField(null=False, blank=False, auto_now=False, auto_now_add=True)

    @property
    def can_edit(self):
        return self.__can_edit

    @can_edit.setter
    def can_edit(self, value):
        self.__can_edit = value

    @property
    def can_delete(self):
        return self.__can_delete

    @can_delete.setter
    def can_delete(self, value):
        self.__can_delete = value