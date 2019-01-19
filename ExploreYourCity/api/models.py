from django.db import models
from django.contrib.auth.models import User as DjangoUser

# TODO: Add relationships between user and other tables


class Region(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField()


class Category(models.Model):
    name = models.CharField(max_length=100)


class Location(models.Model):
    name = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)
    latitude = models.FloatField()
    longitude = models.FloatField()
    # TODO: Add Google Maps related metadata like location ID or address


class Mission(models.Model):
    name = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)


class Objective(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)


class Player(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    score = models.IntegerField()
    friends = models.ManyToManyField('self')
    missions = models.ManyToManyField(Mission)
    objectives_completed = models.ManyToManyField(Objective)

