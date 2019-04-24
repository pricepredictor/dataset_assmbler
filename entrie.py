from enum import Enum


class EntrieType(Enum):
    VACANCY = 'vacancy'
    APARTMENT = 'apartement'
    SHOP = 'shop'
    BUS_STOP = 'bus_stop'
    TRAM_STOP = 'tram_stop'
    SUBWAY_STATION = 'subway_station'
    CAFE = 'cafe'
    OFFICE = 'office'
    POINT_OF_INTEREST = 'point_of_interest'
    SCHOOL = 'school'
    KINDERGARDEN = 'kindergarden'
    HOSPITAL = 'hospital'
    BANK = 'bank'
    UNIVERCITY = 'univercity'
    CINEMA = 'cinema'
    NIGHTLIFE = 'nightlife'
    GOVERNMENT = 'government'
    LEISURE = 'leisure'


class Entrie:
    def __init__(self, coordinates, weight=None):
        self.coorditates = coordinates
        self.weight = weight

    def __repr__(self):
        return f"({self.coorditates[0]}, {self.coorditates[1]}): {self.weight}"
