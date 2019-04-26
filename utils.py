from math import pi, sin, cos, atan2, radians, degrees
from geopy import distance as d

def distance(p1, p2):
    '''Computes distanse in meters between two points with given coordinates'''

    return int(d.distance(p1, p2).km * 1000)


def midpoint(p1, p2):
    '''Computes (lat, lon) midpoint between two points with given coordinates'''

    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)