from django.db import models
from django.contrib.auth.models import User as DjangoUser

# TODO: Add relationships between user and other tables


class Region(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField()

    def __str__(self):
        return f'{self.name} - {self.latitude},{self.longitude} - Radius: {self.radius}km'


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)
    latitude = models.FloatField()
    longitude = models.FloatField()
    # TODO: Add Google Maps related metadata like location ID or address

    def __str__(self):
        return f'{self.name} - {self.latitude},{self.longitude}'

class Mission(models.Model):
    name = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.region} - {self.name}'


class Objective(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f'Mission: {self.mission.name} - Location: {self.location.name}'

class Player(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    score = models.IntegerField()
    friends = models.ManyToManyField('self')
    missions = models.ManyToManyField(Mission)
    objectives_completed = models.ManyToManyField(Objective)

    def __str__(self):
        return self.user.username

