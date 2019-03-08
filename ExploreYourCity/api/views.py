from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
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

    def get_permissions(self):
        if self.request.method == 'POST':
            return []
        return super().get_permissions()


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

        serializer = serializers.PlayerSerializer(request.user.player)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def active_missions(self, request, pk=None):
        """
        Returns a list of specified player's active missions
        """

        try:
            player = models.Player.objects.get(pk=pk)
        except models.Player.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        active_objectives = models.ObjectivePlayer.objects.filter(player__id=player.id, completed=False)

        unique_mission_ids = set()
        for objective in active_objectives:
            unique_mission_ids.add(objective.objective.mission.id)

        unique_missions = []
        for mission_id in list(unique_mission_ids):
            unique_missions.append(models.Mission.objects.get(pk=mission_id))

        serializer = serializers.MissionDetailSerializer(unique_missions, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def completed_missions(self, request, pk=None):
        """
        Returns a list of specified player's completed missions
        """

        try:
            player = models.Player.objects.get(pk=pk)
        except models.Player.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        objective_player_relations = models.ObjectivePlayer.objects.filter(player__id=player.id)

        unique_mission_ids = set()
        for relation in objective_player_relations:
            unique_mission_ids.add(relation.objective.mission.id)

        completed_missions = []
        for mission_id in unique_mission_ids:
            objectives_under_mission = objective_player_relations.filter(objective__mission__id=mission_id)
            completed = True
            for mission_objective in objectives_under_mission:
                if not mission_objective.completed:
                    completed = False
                    break
            if completed:
                mission = models.Mission.objects.get(pk=mission_id)
                completed_missions.append(mission)

        serializer = serializers.MissionDetailSerializer(completed_missions, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def active_objectives(self, request, pk=None):
        """
        Returns a list of specified player's active objectives
        """

        try:
            player = models.Player.objects.get(pk=pk)
        except models.Player.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        objective_player_relations = models.ObjectivePlayer.objects.filter(player__id=player.id, completed=False)

        objectives = []
        for entry in objective_player_relations:
            objectives.append(entry.objective)

        serializer = serializers.ObjectiveDetailSerializer(objectives, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def completed_objectives(self, request, pk=None):
        """
        Returns a list of specified player's completed objectives
        """

        try:
            player = models.Player.objects.get(pk=pk)
        except models.Player.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        objective_player_relations = models.ObjectivePlayer.objects.filter(player__id=player.id, completed=True)

        objectives = []
        for entry in objective_player_relations:
            objectives.append(entry.objective)

        serializer = serializers.ObjectiveDetailSerializer(objectives, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


# /missions/
class MissionViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):

    queryset = models.Mission.objects.all()
    serializer_class = serializers.MissionDetailSerializer

    # TODO: Display missions with objective list correctly

    @action(detail=True, methods=['GET'])
    def objectives(self, request, pk=None):
        """
        Returns a list of objectives belonging to specified mission
        """

        try:
            mission = models.Mission.objects.get(pk=pk)
        except models.Mission.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        objectives = models.Objective.objects.filter(mission__id=mission.id)

        serializer = serializers.ObjectiveDetailSerializer(objectives, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def start(self, request, pk=None):
        """
        Adds the specified mission to current player's list of active missions
        """
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

    # TODO: Don't allow dropping a completed mission
    @action(detail=True, methods=['GET'])
    def drop(self, request, pk=None):
        """
        Drops the specified mission from current player's list of active missions\n
        NOTE: Will currently also remove completed missions
        """
        try:
            mission = models.Mission.objects.get(pk=pk)
        except models.Mission.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        objective_player_relations = models.ObjectivePlayer.objects.filter(objective__mission_id=mission.id)

        for relation in objective_player_relations:
            relation.delete()

        return Response(status=status.HTTP_200_OK)


# /objectives/
class ObjectiveViewSet(mixins.ListModelMixin,  # TODO: Remove ListModelMixin?
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):

    queryset = models.Objective.objects.all()
    serializer_class = serializers.ObjectiveDetailSerializer

    @action(detail=True, methods=['GET'])
    def complete(self, request, pk=None):
        """
        Mark specified objective as complete by current player if in list of active objectives
        """

        try:
            objective = models.Objective.objects.get(pk=pk)
        except models.Objective.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        player = request.user.player

        try:
            objective_player_relation = models.ObjectivePlayer.objects.filter(objective__id=objective.id, player__id=player.id).get()
        except models.ObjectivePlayer.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)

        objective_player_relation.completed = True
        objective_player_relation.save()

        return Response(status=status.HTTP_200_OK)


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
