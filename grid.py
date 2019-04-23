import shapely.geometry
import pyproj

from typing import List
from math import ceil

from utils import midpoint, distance
from entrie import Entrie, EntrieType
from cell import Cell


class Grid:
    def __init__(self, cells: List[List[Cell]]):
        self.cells = cells
        self.dx = distance(cells[0][0].center, cells[0][1].center)
        self.dy = distance(cells[0][0].center, cells[1][0].center)

    def find_suitable_position(self, lat: float, lon: float):
        for i in range(len(self.cells) - 1):
            m = midpoint(self.cells[i][0].center, self.cells[i + 1][0].center)
            if lat > m[0]:
                for j in range(len(self.cells[i]) - 1):
                    m = midpoint(self.cells[i][j].center,
                                 self.cells[i][j + 1].center)
                    if m[1] > lon:
                        return (i, j)

    def get_all_entries_in_radius(self, coordinates, r: float):
        pos = find_suitable_position(*coorditates)
        if pos in None:
            return {}

        i0, j0 = pos
        aggrigated_cell = self.cells[i0][j0]
        i_steps, j_steps = ceil(r / self.dy), ceil(r / self.dx)

        for i in range(max(0, i0 - i_steps), min(len(self.sells), i0 + i_steps + 1)):
            for j in range(max(0, j0 - j_steps), min(len(self.sells[0]), j0 + j_steps + 1)):
                aggrigated_cell += self.cells[i][j]

        return aggrigated_cell.entries

    def add_entrie(self, entrie: Entrie, type: EntrieType):
        pos = find_suitable_position(*entrie.coorditates)
        if not pos is None:
            self.cells[pos[0]][pos[1]].add_entrie(entrie, type)

    def save_cell_centers(self, filename: str):
        with open(f'./tabula-rasa/{filename}', 'w') as file:
            file.write('\n'.join(['; '.join([str(cell.center)
                                             for cell in row]) for row in self.cells]))

    def load_cell_centers(filename: str):
        with open(f'./tabula-rasa/{filename}', 'r') as file:
            rows = file.read().replace('(', '').replace(')', '').split('\n')
        cells = [[Cell(tuple(float(i) for i in c.split(', ')))
                  for c in row.split('; ')] for row in rows]
        return Grid(cells)

    def make_grid_in_degrees(top_left, bottom_right, step=0.0005):
        '''Makes a Grid instance regulary spaced in degrees'''

        lat_max, lon_min = top_left
        lat_min, lon_max = bottom_right

        cells = []
        lon = lon_min
        while lon < lon_max:
            lat, row = lat_min, []
            while lat < lat_max:
                row.append(
                    Cell(midpoint((lat, lon), (lat + step, lon + step))))
                lat += step
            cells.append(row)
            lon += step * 2

        return Grid(cells)

    def make_grid_in_meters(top_left, bottom_right, step=100):
        '''Makes a Grid instance regulary spaced in meters'''

        # Set up projections
        p_ll = pyproj.Proj(init='epsg:4326')
        p_mt = pyproj.Proj(init='epsg:3857')  # metric; same as EPSG:900913

        # Create corners of rectangle to be transformed to a grid
        nw = shapely.geometry.Point(top_left)
        se = shapely.geometry.Point(bottom_right)

        stepsize = step

        # Project corners to target projection
        # Transform NW point to 3857
        s = pyproj.transform(p_ll, p_mt, nw.x, nw.y)
        e = pyproj.transform(p_ll, p_mt, se.x, se.y)  # .. same for SE

        # Iterate over 2D area
        cells = []
        x = s[0]
        while x > e[0]:
            y = s[1]
            row = []
            while y < e[1]:
                nw_point = shapely.geometry.Point(
                    pyproj.transform(p_mt, p_ll, x, y))
                se_point = shapely.geometry.Point(
                    pyproj.transform(p_mt, p_ll, x + stepsize, y + stepsize))
                row.append(
                    Cell(midpoint((nw_point.x, nw_point.y), (se_point.x, se_point.y))))
                y += stepsize * 1.314
            cells.append(row)
            x -= stepsize

        return Grid(cells)
