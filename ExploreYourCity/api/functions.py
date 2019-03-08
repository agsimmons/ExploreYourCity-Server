import math

from . import models

EARTH_RADIUS_IN_KM = 6371


# Calculate distance in km between two coordinates
# https://stackoverflow.com/a/365853
def distance_between_coordinates(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = (math.sin(d_lat / 2) ** 2) + ((math.sin(d_lon / 2) ** 2) * math.cos(lat1) * math.cos(lat2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS_IN_KM * c


# Returns list of completed mission by specified player
def get_completed_missions(player):
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

    return completed_missions


# Returns list of active mission by specified player
def get_active_missions(player):
    active_objectives = models.ObjectivePlayer.objects.filter(player__id=player.id, completed=False)

    unique_mission_ids = set()
    for objective in active_objectives:
        unique_mission_ids.add(objective.objective.mission.id)

    unique_missions = []
    for mission_id in list(unique_mission_ids):
        unique_missions.append(models.Mission.objects.get(pk=mission_id))

    return unique_missions
