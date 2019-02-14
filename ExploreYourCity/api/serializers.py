from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from . import models


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        # TODO: Add validators from settings and remove hardcoded validations
        validators=[UniqueValidator(queryset=User.objects.all())],
        min_length=8,
        max_length=30,
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


class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mission
        fields = ('id', 'name', 'value', 'latitude', 'longitude')

# class UserSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#         required=True,
#         validators=[UniqueValidator(queryset=User.objects.all())]
#     )
#
#     username = serializers.CharField(
#         max_length=32,
#         validators=[UniqueValidator(queryset=User.objects.all())]
#     )
#
#     password = serializers.CharField(
#         min_length=8,
#         write_only=True
#     )
#
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             validated_data['username'],
#             validated_data['email'],
#             validated_data['password']
#         )
#
#         return user
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'password')
#
#
# class CoordinateSerializer(serializers.Serializer):
#     latitude = serializers.FloatField()
#     longitude = serializers.FloatField()
#
#
# class MissionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Mission
#         fields = ('id', 'name', 'value', 'latitude', 'longitude')
#
#
# class MissionDistanceSerializer(serializers.Serializer):
#     distance = serializers.FloatField()
#     mission = MissionSerializer()
#
#
# class RegionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Region
#         fields = '__all__'
#
#
# class MissionDetailSerializer(serializers.ModelSerializer):
#     region = RegionSerializer()
#
#     class Meta:
#         model = models.Mission
#         fields = '__all__'
#
#
# class UsernameSerializer(serializers.Serializer):
#     username = serializers.CharField()
#
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         # TODO: Add associated player's score
#         fields = ('id', 'username')
