from django.db import models
from datetime import date

class Place(models.Model):
    author = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    number_of_seats = models.IntegerField(default=100)
    is_solo = models.BooleanField(default=True)
    description = models.TextField()
    from_date = models.DateField()
    to_date = models.DateField()
    image = models.ImageField(upload_to='images')

    def __str__(self) -> str:
        return f"Place-{self.id}-{self.name}"
    

class PlaceMember(models.Model):
    place_id = models.IntegerField()
    user = models.CharField(max_length=150)


class Place_room(models.Model):
    place_room_id = models.IntegerField(null=True)
    place_room_int = models.CharField(max_length=150)
    # user = models.CharField(max_length=150)

    def __str__(self) -> str:
        return f"Place_room-{self.place_room_id} - "
    

class Place_roomMember(models.Model):
    pr_id = models.IntegerField()
    user = models.CharField(max_length=150)
    from_date = models.DateField()
    to_date = models.DateField()

    def __str__(self) -> str:
        return f"Place_roomMember-{self.user}-{self.pr_id} -"+self.user
    

class FAQMessage(models.Model):
    author = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    message = models.TextField()

    def __str__(self):
        return f"FAQMessage-{self.user} - "+self.author