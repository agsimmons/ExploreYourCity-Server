from django.db import models
from django.contrib.auth.models import User as DjangoUser


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


class Objective(models.Model):
    # Google Maps metadata
    name = models.TextField()

    latitude = models.FloatField()
    longitude = models.FloatField()

    formatted_address = models.TextField()
    google_id = models.TextField()
    place_id = models.TextField()
    reference = models.TextField()

    def __str__(self):
        return f'{self.name} - {self.formatted_address}'


class Mission(models.Model):
    name = models.CharField(max_length=200)  # TODO: Remove?
    value = models.IntegerField()

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    latitude = models.FloatField()
    longitude = models.FloatField()

    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    objectives = models.ManyToManyField(Objective)

    def __str__(self):
        return f'{self.name} - {self.region.name}'


class Player(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    friends = models.ManyToManyField('self', blank=True)

    active_missions = models.ManyToManyField(Mission,
                                             blank=True,
                                             related_name='+')
    completed_missions = models.ManyToManyField(Mission,
                                                blank=True,
                                                related_name='+')

    active_objectives = models.ManyToManyField(Objective,
                                               blank=True,
                                               related_name='+')
    completed_objectives = models.ManyToManyField(Objective,
                                                  blank=True,
                                                  related_name='+')

    def __str__(self):
        return self.user.username
