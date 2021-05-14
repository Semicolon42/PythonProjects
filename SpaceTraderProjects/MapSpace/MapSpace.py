import sys
import threading
import os
import json
import time
import itertools
import math
from SpaceTraderClient import SpaceTraderClient

def current_milli_time():
        return round(time.time() * 1000)

def refresh_system_data(st_client):
    systems_json=st_client.getSystems()
    filename = './system_data.json'
    systems_json['timestamp_last_modified'] = current_milli_time()
    with open(filename, 'w') as outfile:
        json.dump(systems_json, outfile, indent=4)
    print(f"Saved systems data {filename}")
    return systems_json

def load_system_data(st_client):
    system_data_filename = './system_data.json'
    system_data = None
    if (os.path.exists(system_data_filename)):
        print(f"system data exists: {system_data_filename}")
        with open(system_data_filename) as system_data_file:
            system_data = json.load(system_data_file)
        if 'timestamp_last_modified' not in system_data or current_milli_time() - system_data['timestamp_last_modified'] > 1000 * 60 * 60 * 24:
            system_data = refresh_system_data(st_client)
    else:
        system_data = refresh_system_data(st_client)
    return system_data

def location_distance(loc_a, loc_b):
    return math.sqrt((loc_b['y']-loc_a['y'])**2 + (loc_b['x']-loc_a['x'])**2)

def main():
    st_client = SpaceTraderClient('Semicolon42a', '1791656b-d9e4-4e99-90ae-a0b6c6fad301')
    my_locations = dict();

    systems = load_system_data(st_client)
    for system in systems['systems']:
        print("== ", system['symbol'])
        for location in system['locations']:
            print("---- ", location['symbol'], "\t(", location['x'], location['y'], ")")

    distance_table = dict()
    for system in systems['systems']:
        distance_table[system['symbol']] = dict()
        for a in system['locations']:
            distance_table[system['symbol']][a['symbol']] = dict()
            for b in system['locations']:
                distance_table[system['symbol']][ a['symbol'] ][ b['symbol'] ] = location_distance(a, b);
                print("~~~", (system['symbol'], a['symbol'], b['symbol']), distance_table[system['symbol']][a['symbol']][b['symbol']])
    with open('./distance_table.json', 'w') as outfile:
        json.dump(distance_table, outfile, indent=4)

    path_table = dict()
    path_table['timestamp_last_modified'] = current_milli_time()
    for system in systems['systems']:
        path_table[system['symbol']] = dict()
        for a in system['locations']:
            path_table[system['symbol']][a['symbol']] = dict()
            for b in system['locations']:
                path = dict()
                path['timestamp_last_modified'] = current_milli_time()
                path['total_distance'] = distance_table[system['symbol']][ a['symbol'] ][ b['symbol'] ]
                path['path'] = [{"source":a['symbol'], "dest":b['symbol'], "distance": distance_table[system['symbol']][ a['symbol'] ][ b['symbol'] ] }]
                path_table[system['symbol']][ a['symbol'] ][ b['symbol'] ] = path
                print(system['symbol'], a['symbol'] , b['symbol'], path_table[system['symbol']][ a['symbol'] ][ b['symbol'] ] )
    with open('./path_table.json', 'w') as outfile:
        json.dump(path_table, outfile, indent=4)

    print(path_table['OE']['OE-PM']['OE-PM'])


if __name__ == '__main__':
    print('Hello World')
    main()
    print('Goodbye World')