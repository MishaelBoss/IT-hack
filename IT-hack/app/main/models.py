from django.db import models
from datetime import date

class Place(models.Model):
    author = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    places = models.IntegerField(default=100)

    def __str__(self):
        return f"Place-{self.id} - "+self.name
    
class PlaceMember(models.Model):
    place_id = models.IntegerField()
    user = models.CharField(max_length=150)

    def __str__(self):
        return f"PlaceMember-{self.event_id} - "+self.user