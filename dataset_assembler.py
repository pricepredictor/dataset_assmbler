import shapely.geometry
import pyproj
import json
import statistics
import numpy as np
import pandas as pd


from entrie import Entrie, EntrieType
from utils import *


def prepare_table(city_abbr):
    flats = pd.read_csv(
        f'./data/flats/{city_abbr}.csv').drop(columns=['adress', 'subway_station'])
    cols = flats.columns.tolist()
    cols[-1], cols[-2] = cols[-2], cols[-1]
    cols = cols[-2:] + [cols[0]] + cols[1:-2]
    flats = flats[cols]
    flats['price_per_m'] = (
        flats['price'] / flats['area']).map(lambda x: int(x))
    flats = flats.drop(columns=['price'])
    flats['distance_to_center'] = [distance(
        x, city_dict[city_abbr]['center']) for x in zip(flats.latitude, flats.longitude)]
    return flats


def assemble_dataset(city_abbr):
    with open(f'./data/entries/parsed/{city_abbr}.json') as file:
        entry_data = json.load(file)

    flats = prepare_table(city_abbr)

    R = 6371
    feature_list = []
    i = 0
    for row in flats.iterrows():
        i += 1
        row = row[1]
        row_dict = {
            'price_per_m': int(row['price_per_m']),
            'rooms': int(row['rooms']),
            'area': row['area'],
            'floor': int(row['floor']),
            'floors_total': int(row['floors_total']),
            'distance_to_subway': int(row['distance to subway']),
            'distance_to_center': int(row['distance_to_center'])
        }
        lat, lon = row['latitude'], row['longitude']
        for entry_type, entries in zip(entry_data.keys(), entry_data.values()):
            c = np.array([entry[0]
                          for entry in entries if type(entry[0][0]) is float]).T
            d = c.copy()
            d[0] -= lat
            d[0] *= (np.pi / 180)
            d[1] -= lon
            d[1] *= (np.pi / 180)
            a = np.sin(d[0] / 2) * np.sin(d[0] / 2)
            c = 2 * arctan2(np.sqrt(a), np.sqrt(1 - a)) + np.cos(lat * np.pi / 180) * \
                np.cos(c[0] * np.pi / 180) * \
                np.sin(d[1] / 2) * np.sin(d[1] / 2)
            distances = R * c * 1000
            if entry_type == 'shop' and np.nonzero(distances <= 1000)[0].shape[0] == 0:
                break
            for r in [500, 1000]:
                indices = np.nonzero(distances <= r)[0]
                if entry_type in ['vacancy']:
                    salaries = [entries[i][1] for i in indices] or [0]
                    median = int(statistics.median(salaries))
                    mean = int(statistics.mean(salaries))
                    row_dict[f'mean_salaries_{r}'] = mean
                    row_dict[f'median_salaries_{r}'] = median
                row_dict[f'{entry_type}_{str(r)}'] = indices.shape[0]
        else:
            feature_list.append(row_dict)
        if i % 1000 == 0:
            print(i)

    dataset = pd.DataFrame(feature_list)
    dataset.to_csv(f'./datasets/{city_abbr}.csv', index=False)


if __name__ == "__main__":
    assemble_dataset('smr')
