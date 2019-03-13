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

    @action(detail=False, methods=['GET'])
    def friends(self, request):
        """
        Returns a list of friends of the authenticated user
        """

        player = request.user.player
        queryset = player.friends

        serializer = serializers.PlayerSerializer(queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def score(self, request, pk=None):
        """
        Returns score of specified player
        """

        try:
            player = models.Player.objects.get(pk=pk)
        except models.Player.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        completed_missions = functions.get_completed_missions(player)

        score = 0
        for mission in completed_missions:
            score += mission.value

        return Response(data={"score": score}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def active_missions(self, request, pk=None):
        """
        Returns a list of specified player's active missions
        """

        try:
            player = models.Player.objects.get(pk=pk)
        except models.Player.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        active_missions = functions.get_active_missions(player)

        serializer = serializers.MissionDetailSerializer(active_missions, many=True)

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

        completed_missions = functions.get_completed_missions(player)

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

    @action(detail=True, methods=['GET'])
    def remove_friend(self, request, pk=None):
        """
        Removed player specified by {id} from autuhenticated user's friend list\n
        NOTE: Will currently return status 200 regardless of if specified player is a friend or not
        """

        try:
            other_player = models.Player.objects.get(pk=pk)
        except models.Player.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        player = request.user.player
        queryset = player.friends

        # TODO: Validate that player is a friend before removing, although it's fine to not

        queryset.remove(other_player.id)

        return Response(status=status.HTTP_200_OK)


# /missions/
class MissionViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):

    queryset = models.Mission.objects.all()
    serializer_class = serializers.MissionDetailSerializer

    @action(detail=False, methods=['GET'])
    def available(self, request):
        """
        Returns a list of available missions sorted by distance to authenticated player\n
        Pass latitude and longitude in JSON format
        """

        coordinate_serializer = serializers.CoordinateSerializer(data=request.data)

        if coordinate_serializer.is_valid():
            player_coordinates = (coordinate_serializer.validated_data['latitude'],
                                  coordinate_serializer.validated_data['longitude'])

            # Get all missions which have not been started or completed by the player
            all_missions = set(models.Mission.objects.all())
            completed_missions = set(functions.get_completed_missions(request.user.player))
            new_missions = list(all_missions - completed_missions)

            # Calculate distances between player and mission
            mission_distances = []
            for mission in new_missions:
                mission_coordinates = (mission.latitude, mission.longitude)
                distance = functions.distance_between_coordinates(player_coordinates, mission_coordinates)
                mission_distances.append((distance, mission))

            mission_distances_sorted = sorted(mission_distances, key=operator.itemgetter(0))

            missions_sorted = []
            for distance_mission in mission_distances_sorted:
                missions_sorted.append(distance_mission[1])

            mission_serializer = serializers.MissionDetailSerializer(missions_sorted, many=True)

            return Response(data=mission_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(coordinate_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
class ObjectiveViewSet(mixins.RetrieveModelMixin,
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


# /requests/
class RequestViewSet(viewsets.ViewSet):
    def list(self, request):
        player = request.user.player
        queryset = models.Request.objects.filter(request_to=player)

        serializer = serializers.RequestSerializer(queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        player = request.user.player
        try:
            queryset = models.Request.objects.get(pk=pk)
        except models.Request.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Restrict access to recipient
        # NOTE: This allows for side-channel attacks, as requests that exist return 403 without access, and 404 for requests that don't exist
        if queryset.request_to.id != player.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.RequestSerializer(queryset)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def accept(self, request, pk=None):
        player = request.user.player
        try:
            queryset = models.Request.objects.get(pk=pk)
        except models.Request.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Restrict access to recipient
        # NOTE: This allows for side-channel attacks, as requests that exist return 403 without access, and 404 for requests that don't exist
        if queryset.request_to.id != player.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Get from and to players
        from_player = queryset.request_from
        to_player = queryset.request_to

        # Delete request
        queryset.delete()

        # TODO: Check if friend relation already exists when sending the request

        # Add friend relation
        from_player.friends.add(to_player)

        return Response(status=status.HTTP_200_OK)

    # TODO: This should probably be a DELETE request
    @action(detail=True, methods=['GET'])
    def decline(self, request, pk=None):
        player = request.user.player
        try:
            queryset = models.Request.objects.get(pk=pk)
        except models.Request.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Restrict access to recipient
        # NOTE: This allows for side-channel attacks, as requests that exist return 403 without access, and 404 for requests that don't exist
        if queryset.request_to.id != player.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Delete request
        queryset.delete()

        return Response(status=status.HTTP_200_OK)
