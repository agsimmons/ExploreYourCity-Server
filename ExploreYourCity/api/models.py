from django.db import models

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
    category = models.ManyToManyField(Category)
    latitude = models.FloatField()
    longitude = models.FloatField()
    # TODO: Add Google Maps related metadata like location ID or address


class Mission(models.Model):
    name = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)


class Objective(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

