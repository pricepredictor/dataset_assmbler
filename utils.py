from math import pi, sin, cos, atan2, radians, degrees

def distance(p1, p2):
    '''Computes distanse in meters between two points with given coordinates'''
    
    lat1, lon1 = p1
    lat2, lon2 = p2
    R = 6378.137 # Earth's radius in KM

    dLat = lat2 * pi / 180 - lat1 * pi / 180
    dLon = lon2 * pi / 180 - lon1 * pi / 180
    a = sin(dLat / 2) * sin(dLat / 2) + cos(lat1 * pi / 180) * cos(lat2 * pi / 180) * sin(dLon / 2) * sin(dLon / 2)
    c = 2 * atan2(a ** 0.5, (1 - a) ** 0.5)
    d = R * c
    return d * 1000


def midpoint(p1, p2):
    '''Computes (lat, lon) midpoint between two points with given coordinates'''

    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)