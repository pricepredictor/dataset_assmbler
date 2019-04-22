import shapely.geometry
import pyproj

from utils import midpoint
from entrie import Entrie, EntrieType 
from cell import Cell

class Grid:
    def __init__(self, cells):
        self.cells = cells

    def add_entrie(self, entrie: Entrie, type: EntrieType):
        c = entrie.coorditates
        for i in range(len(self.cells) - 1):
            m = midpoint(self.cells[i][0].center, self.cells[i + 1][0].center)
            if c[0] > m[0]:
                for j in range(len(self.cells[i]) - 1):
                    m = midpoint(self.cells[i][j].center, self.cells[i][j + 1].center)
                    if m[1] > c[1]:
                        self.cells[i][j].add_entrie(entrie, type)
                        return i, j

    def save_cell_centers(self, filename: str):
        with open(f'./tabula-rasa/{filename}', 'w') as file:
            file.write('\n'.join(['; '.join([str(cell.center) for cell in row]) for row in self.cells]))

    def load_cell_centers(filename: str):
        with open(f'./tabula-rasa/{filename}', 'r') as file:
            rows = file.read().replace('(', '').replace(')', '').split('\n')
        cells = [[Cell(tuple(float(i) for i in c.split(', '))) for c in row.split('; ')] for row in rows]
        return Grid(cells)

    def make_grid(top_left, bottom_right, initial_size=100):
        '''Factory method for creating Grid instances'''
        
        # Set up projections
        p_ll = pyproj.Proj(init='epsg:4326')
        p_mt = pyproj.Proj(init='epsg:3857') # metric; same as EPSG:900913

        # Create corners of rectangle to be transformed to a grid
        nw = shapely.geometry.Point(top_left)
        se = shapely.geometry.Point(bottom_right)

        stepsize = initial_size

        # Project corners to target projection
        s = pyproj.transform(p_ll, p_mt, nw.x, nw.y) # Transform NW point to 3857
        e = pyproj.transform(p_ll, p_mt, se.x, se.y) # .. same for SE

        # Iterate over 2D area
        cells = []
        x = s[0]
        while x > e[0]:
            y = s[1]
            row = []
            while y < e[1]:
                nw_point = shapely.geometry.Point(pyproj.transform(p_mt, p_ll, x, y))
                se_point = shapely.geometry.Point(pyproj.transform(p_mt, p_ll, x + stepsize, y + stepsize))
                row.append(Cell(midpoint((nw_point.x, nw_point.y), (se_point.x, se_point.y))))
                y += stepsize
            cells.append(row)
            x -= stepsize

        return Grid(cells)