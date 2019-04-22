from enum import Enum

from utils import midpoint
from entrie import Entrie, EntrieType

class CellTypes(Enum):
    URBAN = 1
    PARK = 2
    WATER = 3


class Cell:
    def __init__(self, center):
        self.center = center
        self.type = CellTypes.URBAN
        self.entries = {
            EntrieType.VACANCY: [], 
            EntrieType.APARTMENT: [], 
            EntrieType.SHOP: [], 
            EntrieType.BUS_STOP: [], 
            EntrieType.TRAM_STOP: [], 
            EntrieType.SUBWAY_STATION: [], 
            EntrieType.CAFE: [], 
            EntrieType.OFFICE: [], 
            EntrieType.POINT_OF_INTEREST: [], 
        }

    def add_entrie(self, entrie: Entrie, type: EntrieType):
        self.entries[type].append(entrie)

    def __add__(self, other):
        res = Cell(midpoint(self.center, other.center))
        for type in self.entries:
            res.entries[type] = self.entries[type] + other.entries[type]
        return res

    def __repr__(self):
        return f"{self.center[0]}, {self.center[1]}"
