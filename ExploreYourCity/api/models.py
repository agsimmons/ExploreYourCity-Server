from django.db import models
from django.contrib.auth.models import User as DjangoUser

from django.db.models.signals import post_save
from django.dispatch import receiver


class Region(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField()

    def __str__(self):
        return f'{self.name} - {self.latitude},{self.longitude} - Radius: {self.radius}km'


# https://developers.google.com/places/supported_types
class Type(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    types = models.ManyToManyField(Type)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Location(models.Model):
    categories = models.ManyToManyField(Category)

    # Google Maps metadata
    name = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    formatted_address = models.TextField()
    google_id = models.TextField()
    place_id = models.TextField()
    reference = models.TextField()

    def __str__(self):
        return f'{self.name} - {self.latitude},{self.longitude}'


class Mission(models.Model):
    name = models.CharField(max_length=200)
    value = models.IntegerField()

    latitude = models.FloatField()
    longitude = models.FloatField()

    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.region.name}'


class Objective(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f'Mission: {self.mission.name} - Location: {self.location.name}'


class Player(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    friends = models.ManyToManyField('self', blank=True)
    missions = models.ManyToManyField(Mission, blank=True)
    objectives_completed = models.ManyToManyField(Objective, blank=True)

    def __str__(self):
        return self.user.username


# When a User is created, create a corresponding Player with a OneToOne relationship to the created User
@receiver(post_save, sender=DjangoUser)
def create_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
