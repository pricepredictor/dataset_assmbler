import shapely.geometry
import pyproj
import json
import statistics
import numpy as np
import pandas as pd


#from grid import Grid
#from cell import Cell
from entrie import Entrie, EntrieType 
from utils import *

def save_houses(city_abbr):
    reverse_tagged = pd.read_csv(f'./data/reversed/{city_abbr}.csv')

    houses_dict = {}
    for i, row in reverse_tagged.iterrows():
        house = {'floors': 0, 'price_per_m': 0, 'year': 0, 'latitude': 0, 'longitude': 0}
        house['latitude'] = row.latitude
        house['longitude'] = row.longitude
        house['year'] = int(float(row.year)) if row.year != 'nan' and row.year != '1.0' and row.year != '0' and row.year != 'None' and not np.isnan(float(row.year)) else 0
        house['price_per_m'] = int(float(row.price) / float(row.area) // 1000)
        house['floors'] = int(row.floor.split('/')[0])
        if row.adress in houses_dict:
            houses_dict[row.adress].append(house)
        else:
            houses_dict[row.adress] = [house]

    floors = []
    price_per_m = []
    year = []
    latitude = []
    longitude = []
    for addr, flats in zip(houses_dict.keys(), houses_dict.values()):
        ppm = [flat['price_per_m'] for flat in flats]
        price_per_m.append(round(sum(ppm) / len(ppm), 1))
        latitude.append(flats[0]['latitude'])
        longitude.append(flats[0]['longitude'])

        y = None
        f = None
        for flat in flats:
            if flat['year']:
                y = int(flat['year'])
            if flat['floors']:
                f = (flat['floors'])
        year.append(y)
        floors.append(f)

    houses = pd.DataFrame()
    houses['floors'] = floors
    houses['price_per_m'] = price_per_m
    houses['year'] = year
    houses['latitude'] = latitude
    houses['longitude'] = longitude
        
    with_age = []
    for house in [h for i, h in houses.iterrows() if not np.isnan(h.year)]:
        with_age.append([[round(house.latitude, 6), round(house.longitude, 6)], 2019 - int(house.year)])

    with_floors = []
    for house in [h for i, h in houses.iterrows() if not np.isnan(h.floors)]:
        with_floors.append([[round(house.latitude, 6), round(house.longitude, 6)], 2019 - int(house.floors)])

    with_price= []
    for house in [h for i, h in houses.iterrows()]:
        with_price.append([[round(house.latitude, 6), round(house.longitude, 6)], (house.price_per_m)])

    lats, lons, ppms = [], [], []
    for house in [h for i, h in houses.iterrows()]:
        lats.append(round(house.latitude, 6))
        lons.append(round(house.longitude, 6))
        ppms.append(house.price_per_m)

    hs = pd.DataFrame()
    hs['price_per_m'] = ppms
    hs['latitude'] = lats
    hs['longitude'] = lons

    hs.to_csv(f'./data/houses/{city_abbr}.csv', index=False)

    with open(f'./data/entries/parsed/{city_abbr}.json') as file:
        entries = json.load(file)

    entries['with_age'] = with_age
    entries['with_floors'] = with_floors
    entries['with_price'] = with_price

    with open(f'./data/entries/with_houses/{city_abbr}.json', 'w') as outfile:  
        json.dump(entries, outfile)
    
    return True


if __name__ == '__main__':
    houses = save_houses('smr')