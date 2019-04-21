from enum import Enum

class EntrieType(Enum):
    VACANCY = 1
    APARTMENT = 2
    SHOP = 3
    BUS_STOP = 4
    TRAM_STOP = 5
    SUBWAY_STATION = 6
    CAFE = 7
    OFFICE = 8
    POINT_OF_INTEREST = 9

class Entrie:
    def __init__(self, coordinates, weight=None):
        self.coorditates = coordinates
        self.weight = weight

    def __repr__(self):
        return f"({self.coorditates[0]}, {self.coorditates[1]}): {self.weight}"