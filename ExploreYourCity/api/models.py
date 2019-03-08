from django.db import models
from django.contrib.auth.models import User as DjangoUser


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


class Mission(models.Model):
    value = models.IntegerField()

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f'{self.category.name} - {self.id}'


class Objective(models.Model):
    name = models.TextField()

    latitude = models.FloatField()
    longitude = models.FloatField()

    formatted_address = models.TextField()
    gmaps_id = models.TextField()

    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.formatted_address}'


class Player(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username


class ObjectivePlayer(models.Model):
    class Meta:
        unique_together = (('player', 'objective'),)

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    objective = models.ForeignKey(Objective, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.objective.__str__()} - {self.player.__str__()} - Completed: {self.completed}'
