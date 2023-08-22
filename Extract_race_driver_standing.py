import pandas as pd
import numpy as np
import requests
from Extract_race_result import rounds, extract_race_result
import os

# print("******************************Calling Result function***********************************")
# results, rounds = extract_race_result()
# print(results.shape)
# print(len(rounds))

file_path = 'D:/DATA_ANALYTICS/Race_Analysis/results.csv'
print(file_path)
file_exists = os.path.isfile(file_path)
print(file_exists)
if (file_exists):
    results = pd.read_csv('results.csv')
    print("#####################################")
    print(results.shape)
    rounds1 = rounds
    print(len(rounds1))
else:
    print("******************************Calling result function***********************************")
    results, rounds1 = extract_race_result()
    print(results.shape)


driver_standings = {'season': [],
                    'round': [],
                    'driver': [],
                    'driver_points': [],
                    'driver_wins': [],
                    'driver_standings_pos': []}

# query API

for n in list(range(len(rounds1))):
    print("******************************Inside for loop range len of rounds***********************************")
    for i in rounds1[n][1]:    # iterate through rounds of each year

        url = 'https://ergast.com/api/f1/{}/{}/driverStandings.json'
        raw = requests.get(url.format(rounds1[n][0], i))
        json = raw.json()
        print(json['MRData']['StandingsTable']['StandingsLists'][0]['round'])
        print(json['MRData']['StandingsTable']['StandingsLists'][0]['season'])

        for item in json['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']:
            # print("******************************Inside item loop***********************************")
            try:
                driver_standings['season'].append(
                    int(json['MRData']['StandingsTable']['StandingsLists'][0]['season']))
            except:
                driver_standings['season'].append(None)

            try:
                driver_standings['round'].append(
                    int(json['MRData']['StandingsTable']['StandingsLists'][0]['round']))
            except:
                driver_standings['round'].append(None)

            try:
                driver_standings['driver'].append(item['Driver']['driverId'])
            except:
                driver_standings['driver'].append(None)

            try:
                driver_standings['driver_points'].append(int(item['points']))
            except:
                driver_standings['driver_points'].append(None)

            try:
                driver_standings['driver_wins'].append(int(item['wins']))
            except:
                driver_standings['driver_wins'].append(None)

            try:
                driver_standings['driver_standings_pos'].append(
                    int(item['position']))
            except:
                driver_standings['driver_standings_pos'].append(None)

driver_standings = pd.DataFrame(driver_standings)
print(driver_standings.shape)
driver_standings.to_csv('driver_standing.csv', index=False)
# define lookup function to shift points and number of wins from previous rounds


def lookup(df, team, points):
    df['lookup1'] = df.season.astype(str) + df[team] + df['round'].astype(str)
    df['lookup2'] = df.season.astype(
        str) + df[team] + (df['round']-1).astype(str)
    new_df = df.merge(df[['lookup1', points]], how='left',
                      left_on='lookup2', right_on='lookup1')
    new_df.drop(['lookup1_x', 'lookup2', 'lookup1_y'], axis=1, inplace=True)
    new_df.rename(columns={points+'_x': points +
                  '_after_race', points+'_y': points}, inplace=True)
    new_df[points].fillna(0, inplace=True)
    return new_df


driver_standings = lookup(driver_standings, 'driver', 'driver_points')
driver_standings = lookup(driver_standings, 'driver', 'driver_wins')
driver_standings = lookup(driver_standings, 'driver', 'driver_standings_pos')

driver_standings.drop(['driver_points_after_race', 'driver_wins_after_race', 'driver_standings_pos_after_race'],
                      axis=1, inplace=True)
