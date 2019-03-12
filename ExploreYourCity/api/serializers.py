from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from . import models


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        # TODO: Add validators from settings and remove hardcoded validations
        validators=[UniqueValidator(queryset=User.objects.all())],
        min_length=8,
        max_length=24,
    )
    password = serializers.CharField(
        # TODO: Add validators from settings and remove hardcoded validations
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class CoordinateSerializer(serializers.Serializer):
    latitude = serializers.FloatField(min_value=-90.0,
                                      max_value=90.0)

    longitude = serializers.FloatField(min_value=-180.0,
                                       max_value=180.0)

class PlayerSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username')

    class Meta:
        model = models.Player
        fields = ('id', 'username', 'score')


class ObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Objective
        fields = ('id', 'name')


class ObjectiveDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Objective
        fields = ('id', 'name', 'formatted_address', 'latitude', 'longitude')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'name')


class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mission
        fields = ('id',)


class MissionDetailSerializer(serializers.ModelSerializer):

    category = CategorySerializer()

    class Meta:
        model = models.Mission
        fields = ('id', 'category')
