from django.db import models

class Event(models.Model):
    organizer = models.ForeignKey('SideMountUser', on_delete=models.CASCADE, related_name='events')
    description = models.CharField(max_length=155)
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    location = models.CharField(max_length=100)
    attendees = models.ManyToManyField('SideMountUser', through='Attendee')
    image_url = models.TextField()
    gi = models.ForeignKey('Gi', on_delete=models.CASCADE)


    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value