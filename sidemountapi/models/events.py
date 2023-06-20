from django.db import models

class Event(models.Model):
    organizer = models.ForeignKey('SideMountUser', on_delete=models.CASCADE, related_name='events')
    description = models.CharField(max_length=250)
    title = models.CharField(max_length=150)
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    location = models.CharField(max_length=100)
    attendees = models.ManyToManyField('SideMountUser', through='Attendee', related_name="events_attending")
    image_url = models.TextField()
    requirements = models.CharField(max_length=350, default='No requirements')
    gi = models.ForeignKey('Gi', on_delete=models.CASCADE)


    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value

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