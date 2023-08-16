import pandas as pd
import requests
import numpy as np

races = {
    'season': [],
    'round': [],
    'circuit_id': [],
    'lateral': [],
    'longitude': [],
    'country': [],
    'date': [],
    'url': []
}

for year in list(range(1950, 2023)):

    url = 'https://ergast.com/api/f1/{}.json'
    r = requests.get(url.format(year))
    json = r.json()
    # print(json)

    for item in json['MRData']['RaceTable']['Races']:
        try:
            races['season'].append(int(item['season']))
        except:
            races['season'].append(None)

        try:
            races['round'].append(int(item['round']))
        except:
            races['round'].append(None)

        try:
            races['circuit_id'].append(item['Circuit']['circuitId'])
        except:
            races['circuit_id'].append(None)

        try:
            races['lateral'].append(float(item['Circuit']['Location']['lat']))
        except:
            races['lateral'].append(None)

        try:
            races['longitude'].append(
                float(item['Circuit']['Location']['long']))
        except:
            races['longitude'].append(None)

        try:
            races['country'].append(item['Circuit']['Location']['country'])
        except:
            races['country'].append(None)

        try:
            races['date'].append(item['date'])
        except:
            races['date'].append(None)

        try:
            races['url'].append(item['url'])
        except:
            races['url'].append(None)

races = pd.DataFrame(races)
print(races.shape)
races.to_csv('races.csv', index=False)
