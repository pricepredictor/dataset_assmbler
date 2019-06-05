import json
from entrie import EntrieType, Entrie

city_name = 'smr'

with open(f'./data/entries/raw/{city_name}.json', 'r') as f:
    raw = json.load(f)

keyword_dict = {
    'shop': ['shop'],
    'bus_stop': ['public_transport'],
    'tram_stop': ['tram_stop'],
    'subway_station': ['subway_station'],
    'cafe': ['fast_food', 'cafe', 'restaurant'],
    'office': ['office'],
    'point_of_interest': ['place_of_worship', 'fountain', 'library', 'theatre', 'monument', 'memorial', 'artwork'],
    'school': ['school'],
    'hospital': ['clinic', 'hospital'],
    'bank': ['bank'],
    'univercity': ['university'],
    'cinema': ['cinema'],
    'nightlife': ['nightclub', 'stripclub', 'pub', 'bar'], 
    'government': ['courthouse', 'register_office', 'townhall', 'public_building', 'police'],
    'leisure': ['sport_center', 'fitness_centre'],
    'hotel': ['motel', 'hotel', 'hostel']
}

parsed_entries = {
    key: [] for key in keyword_dict.keys()
}

for entrie_type, keywords in zip(keyword_dict. keys(), keyword_dict.values()):
    for keyword in keywords:
        parsed_entries[entrie_type] += [[[e[0][1], e[0][0]]] for e in raw[keyword] if len(e[0]) == 2]

with open(f'./data/vacancies/{city_name}.csv') as file:
    vacancy_data = file.read()

parsed_entries['vacancy'] = []
for vacancy_line in vacancy_data.split('\n'):
    vacancy = vacancy_line.split('; ')
    lat, lon = [float(c) for c in vacancy[-2].split(', ')]
    parsed_entries['vacancy'].append([[lat, lon], int(vacancy[-1])])

with open(f'./data/entries/parsed/{city_name}.json', 'w') as f:
    raw = json.dump(parsed_entries, f)

parsed_entries.keys()

len(parsed_entries['subway_station'])


