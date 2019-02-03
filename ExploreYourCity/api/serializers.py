from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from . import models


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    username = serializers.CharField(
        max_length=32,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        min_length=8,
        write_only=True
    )

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )

        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class CoordinateSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mission
        fields = ('id', 'name', 'value', 'latitude', 'longitude')


class MissionDistanceSerializer(serializers.Serializer):
    distance = serializers.FloatField()
    mission = MissionSerializer()

