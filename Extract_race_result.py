import pandas as pd
import numpy as np
import requests
from Extract_race_venue import extract_race_venue
import os
from pathlib import Path

# print("******************************Calling Venue function***********************************")
# races = extrct_race_venue()

file_path = 'D:/DATA_ANALYTICS/Race_Analysis/races.csv'
print(file_path)
file_exists = os.path.isfile(file_path)
if (file_exists):
    races = pd.read_csv('races.csv')
    print(races.shape)
else:
    print("******************************Calling Venue function***********************************")
    races = extract_race_venue()

rounds = []
for year in np.array(races.season.unique()):
    rounds.append([year, list(races[races.season == year]['round'])])


def extract_race_result():
    # rounds = []
    # for year in np.array(races.season.unique()):
    #     rounds.append([year, list(races[races.season == year]['round'])])

    # query API

    results = {'season': [],
               'round': [],
               'circuit_id': [],
               'driver': [],
               'date_of_birth': [],
               'nationality': [],
               'constructor': [],
               'grid': [],
               'time': [],
               'status': [],
               'points': [],
               'podium': []}

    for n in list(range(len(rounds))):
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        for i in rounds[n][1]:
            print(n)

            url = 'http://ergast.com/api/f1/{}/{}/results.json'
            r = requests.get(url.format(rounds[n][0], i))
            json = r.json()

            for item in json['MRData']['RaceTable']['Races'][0]['Results']:
                try:
                    results['season'].append(
                        int(json['MRData']['RaceTable']['Races'][0]['season']))
                except:
                    results['season'].append(None)

                try:
                    results['round'].append(
                        int(json['MRData']['RaceTable']['Races'][0]['round']))
                except:
                    results['round'].append(None)

                try:
                    results['circuit_id'].append(
                        json['MRData']['RaceTable']['Races'][0]['Circuit']['circuitId'])
                except:
                    results['circuit_id'].append(None)

                try:
                    results['driver'].append(item['Driver']['driverId'])
                except:
                    results['driver'].append(None)

                try:
                    results['date_of_birth'].append(
                        item['Driver']['dateOfBirth'])
                except:
                    results['date_of_birth'].append(None)

                try:
                    results['nationality'].append(
                        item['Driver']['nationality'])
                except:
                    results['nationality'].append(None)

                try:
                    results['constructor'].append(
                        item['Constructor']['constructorId'])
                except:
                    results['constructor'].append(None)

                try:
                    results['grid'].append(int(item['grid']))
                except:
                    results['grid'].append(None)

                try:
                    results['time'].append(int(item['Time']['millis']))
                except:
                    results['time'].append(None)

                try:
                    results['status'].append(item['status'])
                except:
                    results['status'].append(None)

                try:
                    results['points'].append(int(item['points']))
                except:
                    results['points'].append(None)

                try:
                    results['podium'].append(int(item['position']))
                except:
                    results['podium'].append(None)

    results = pd.DataFrame(results)
    # print(results.shape)
    results.to_csv('results.csv', index=False)
    return results, rounds
