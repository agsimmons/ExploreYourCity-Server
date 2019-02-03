import math

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

    return EARTH_RADIUS_IN_KM * c;
