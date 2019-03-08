from rest_framework import status, viewsets, mixins
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import rest_framework.permissions
from rest_framework.decorators import action
from django.contrib.auth.models import User
from . import serializers
from . import models
from . import functions

import operator


# /users/
class UserViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    @action(detail=False, methods=['DELETE'])
    def remove_account(self, request):
        """
        Deletes authenticated player's account
        """

        request.user.delete()

        return Response(status=status.HTTP_200_OK)


# /players/
class PlayerViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):

    queryset = models.Player.objects.all()
    serializer_class = serializers.PlayerSerializer

    @action(detail=False, methods=['GET'])
    def myself(self, request):
        """
        If authentication credentials are valid, status 200 and {'id': int} is returned.\n
        If authentication credentials are invalid, status 401
        """

        return Response({'id': request.user.player.id}, status=status.HTTP_200_OK)

    # # TODO: Update for new mission/objective format
    # @action(detail=True, methods=['GET'])
    # def active_missions(self, request, pk=None):
    #     """
    #     Returns a list of specified player's active missions
    #     """
    #
    #     try:
    #         player = models.Player.objects.get(pk=pk)
    #     except models.Player.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #
    #     missions = player.active_missions.all()
    #
    #     serializer = serializers.MissionSerializer(missions, many=True)
    #
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)
    #
    # # TODO: Update for new mission/objective format
    # @action(detail=True, methods=['GET'])
    # def completed_missions(self, request, pk=None):
    #     """
    #             Returns a list of specified player's completed missions
    #      """
    #
    #     try:
    #         player = models.Player.objects.get(pk=pk)
    #     except models.Player.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #
    #     missions = player.completed_missions.all()
    #
    #     serializer = serializers.MissionSerializer(missions, many=True)
    #
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)
    #
    # # TODO: Update for new mission/objective format
    # @action(detail=True, methods=['GET'])
    # def active_objectives(self, request, pk=None):
    #     try:
    #         player = models.Player.objects.get(pk=pk)
    #     except models.Player.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #
    #     objectives = player.active_objectives.all()
    #
    #     serializer = serializers.ObjectiveSerializer(objectives, many=True)
    #
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)
    #
    # # TODO: Update for new mission/objective format
    # @action(detail=True, methods=['GET'])
    # def completed_objectives(self, request, pk=None):
    #     try:
    #         player = models.Player.objects.get(pk=pk)
    #     except models.Player.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #
    #     objectives = player.completed_objectives.all()
    #
    #     serializer = serializers.ObjectiveSerializer(objectives, many=True)
    #
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.request.method == 'POST':
            return []
        return super().get_permissions()


# /missions/
class MissionViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):

    queryset = models.Mission.objects.all()
    serializer_class = serializers.MissionDetailSerializer

    # TODO: Display missions with objective list correctly

    @action(detail=True, methods=['GET'])
    def start(self, request, pk=None):
        try:
            mission = models.Mission.objects.get(pk=pk)
        except models.Mission.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        objectives = models.Objective.objects.filter(mission__id=mission.id)

        player = request.user.player

        # TODO: Check if mission is already active or completed. Abstract this to functions.py

        for objective in objectives:
            objective_player = models.ObjectivePlayer(objective=objective, player=player)
            objective_player.save()

        return Response(status=status.HTTP_200_OK)


# /objectives/
class ObjectiveViewSet(mixins.ListModelMixin,  # TODO: Remove ListModelMixin?
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):

    queryset = models.Objective.objects.all()
    serializer_class = serializers.ObjectiveDetailSerializer


# # Get missions sorted by distance from user
# # GET
# # /missions
# # Body:
# #     latitude: current latitude
# #     longitude: current longitude
# class Missions(APIView):
#     def get(self, request, format=None):
#         coordinate_serializer = serializers.CoordinateSerializer(data=request.data)
#
#         # If passed latitude and longitude is valid
#         if coordinate_serializer.is_valid():
#             lat = coordinate_serializer.validated_data['latitude']
#             lon = coordinate_serializer.validated_data['longitude']
#
#             missions = models.Mission.objects.all()
#             mission_distance_list = []
#             for mission in missions:
#                 distance = functions.distance_between_coordinates((lat, lon),
#                                                                   (mission.latitude, mission.longitude))
#                 mission_distance_list.append((distance, mission))
#             mission_distance_list.sort(key=operator.itemgetter(0))
#
#             return_mission_list = []
#             for mission in mission_distance_list:
#                 return_mission_list.append({
#                     'distance': mission[0],
#                     'mission': mission[1]
#                 })
#
#             mission_distance_serializer = serializers.MissionDistanceSerializer(return_mission_list, many=True)
#             return Response(mission_distance_serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(coordinate_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
