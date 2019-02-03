from rest_framework import status, viewsets
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import rest_framework.permissions
from . import serializers
from . import models
from . import functions

import operator


# Register a new user account
# /register
# Body:
#     username: New user username
#     password: New user password
#     email: New user email
class UserRegister(APIView):
    permission_classes = (rest_framework.permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # TODO: Deactivate user account and send verification email which re-activates account
            # user.is_active = False
            # user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get missions sorted by distance from user
# /missions
# Body:
#     latitude: current latitude
#     longitude: current longitude
class Missions(APIView):
    def get(self, request, format=None):
        coordinate_serializer = serializers.CoordinateSerializer(data=request.data)

        # If passed latitude and longitude is valid
        if coordinate_serializer.is_valid():
            lat = coordinate_serializer.validated_data['latitude']
            lon = coordinate_serializer.validated_data['longitude']

            missions = models.Mission.objects.all()
            mission_distance_list = []
            for mission in missions:
                distance = functions.distance_between_coordinates((lat, lon),
                                                                  (mission.latitude, mission.longitude))
                mission_distance_list.append((distance, mission))
            mission_distance_list.sort(key=operator.itemgetter(0))

            return_mission_list = []
            for mission in mission_distance_list:
                return_mission_list.append({
                    'distance': mission[0],
                    'mission': mission[1]
                })

            mission_distance_serializer = serializers.MissionDistanceSerializer(return_mission_list, many=True)
            return Response(mission_distance_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(coordinate_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get details of specific mission
# /missions/<int:pk>
class MissionsDetail(APIView):
    def get(self, request, pk, format=None):
        try:
            mission = models.Mission.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.MissionDetailSerializer(mission)
        return Response(serializer.data, status=status.HTTP_200_OK)
