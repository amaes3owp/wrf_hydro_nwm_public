# -*- coding: utf-8 -*-
"""NHD Network traversal

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ocgg1JiOGBUl3jfSUPCEVnW5WNaqLKCD

See simple test example [here](https://colab.research.google.com/drive/1wrCl6bTQWNVMQj0U54vVdXMOx4mDf5_d#scrollTo=cOZV2reX1zDJ)<br><br>
NHD analysis from GIS (based on channels_nwm_v12_routeLink)
Total number of channel segments: 2,729,077
Order 10 terminal segments:   1  (total: 441)             1 Running total of terminal segments
Order 9 terminal segments:    2  (total: 3,334)           3
Order 8 terminal segments:    4  (total: 7,495)           7
Order 7 terminal segments:   31  (total: 20,956)         38
Order 6 terminal segments:   87  (total: 48,275)        125
Order 5 terminal segments:  230  (total: 91,386)        355
Order 4 terminal segments:  987  (total: 170,417)     1,342
Order 3 terminal segments: 1972  (total: 315,289)     3,314
Order 2 terminal segments: 5788  (total: 598,992)     9,102
Order 1 terminal segments: 5611  (total: 1,472,492)  14,713

##Define functions
"""
import time
class network():
    def __init__(self):
        self.networkID = None
        self.reachCollection = None
        head_segments = []

class reach():
    def __init__(self):
        self.reachID = None
        self.nodeCollection = None

class segment():
    def __init__(self):
        self.segmentID = None
        self.length = -1

def get_leaves_from_trunk():
    '''
    Define a function to assign leaves of a given nodeset
    '''
    pass

# NOTE: these methods can lose the "connections" and "rows" arguments when
# implemented as class methods where those arrays are members of the class.
def recurse_downstream(key, rows, key_col, downstream_col, length_col, down_connections, terminal_code):
    for row in rows:
        # print(f'{key_col}  {key}')
        if row[key_col] == key:
            down_connections[key] = {'downstream': row[downstream_col], 'length': row[length_col] }
            if not key == terminal_code:
                recurse_downstream(row[downstream_col], rows, key_col, downstream_col, length_col, down_connections, terminal_code)

def determine_keys(rows, key_col, downstream_col, terminal_code
            , verbose = False, debuglevel = 0):
    # Get the upstream nodes to start with
    if verbose: print('starting build')
    if verbose: print('all_keys')
    all_keys = [row[key_col] for row in rows]
    if debuglevel == -1: print(f'length = {len(all_keys)}')
    if verbose: print('all_keys complete')
    if debuglevel == -2: print(all_keys)
    if verbose: print('ref_keys')
    ref_keys = [row[downstream_col] for row in rows]
    if verbose: print('ref_keys complete')
    if debuglevel == -2: print(ref_keys)
    if verbose: print('headwater_keys')
    headwater_keys = [x for x in all_keys if x not in ref_keys]
    if debuglevel == -2: print(headwater_keys)
    if verbose: print('headwater_keys complete')

    # Get the downstream terminating nodes
    if verbose: print('terminal_keys')
    terminal_keys = []
    for row in rows:
        if row[downstream_col] == terminal_code:
            terminal_keys.append(row[key_col])
    if debuglevel == -2: print(terminal_keys)
    if verbose: print('terminal_keys complete')

    return all_keys, ref_keys, headwater_keys, terminal_keys

def build_connections(rows, key_col, downstream_col, length_col, terminal_code
                    , headwater_keys, terminal_keys
                    , verbose = False, debuglevel = 0):
    # Recursive call to go all the way down the relationship
    up_connections = {}
    down_connections = {}

    if verbose: print('\nStart Recursion')
    if verbose: print('down_connections')
    for key in headwater_keys:
        recurse_downstream(key = key
             , rows = rows
             , key_col = key_col
             , downstream_col = downstream_col
             , length_col = length_col
             , down_connections = down_connections
             , terminal_code = terminal_code)
    if debuglevel == -2: print(down_connections)
    if verbose: print('down_connections complete')

    # Create inverse of connections looking upstream
    if verbose: print('up_connections')
    for i in headwater_keys:
        up_connections[i] = { 'upstreams': [terminal_code], 'length': down_connections[i]['length'] }

    for i in down_connections.keys():
        if not down_connections[i]['downstream'] == terminal_code:
            up_connections[down_connections[i]['downstream']] = { 'upstreams': [], 'length': down_connections[i]['length'] }
                                    #  `down_connections[down_connections[i]['downstream']]['length']` to just `down_connections[i]['length']`
            for j in down_connections.keys():
                if down_connections[i]['downstream'] == down_connections[j]['downstream']:
                    up_connections[down_connections[i]['downstream']]['upstreams'].append(j)
    if debuglevel == -2: print(up_connections)
    if verbose: print('up_connections complete')

    return down_connections, up_connections

def rec_print_down(key, down_connections, terminal_code, debuglevel = 0):
    if key == terminal_code: return

    print(f"{key} with length {down_connections[key]['length']}")
    rec_print_down(down_connections[key]['downstream'], down_connections, terminal_code)

def rec_print_up(keys, tab_count, up_connections, down_connections, terminal_code, debuglevel = 0):
    if not isinstance(keys, list): keys = [keys]
    tab_count += 1
    for key in keys:
        if not key == terminal_code:
            print(f"{'.' * (tab_count)}\\{key} with length {down_connections[key]['length']}\\")
            rec_print_up(up_connections[key]['upstreams'], tab_count, up_connections, down_connections, terminal_code)

def print_connections(headwater_keys = None, terminal_keys = None
                    , down_connections = None, up_connections = None
                    , terminal_code = None):
    try:
        if headwater_keys:
            print("########################")
            print("Downstream Connections")
            print("########################")
            for key in headwater_keys:
                rec_print_down(key, down_connections, terminal_code)
                print("########################")

        if terminal_keys:
            print("########################")
            print("Upstream Connections")
            print("########################")
            for key in terminal_keys:
                rec_print_up([key], -1, up_connections, down_connections, terminal_code)
                print("########################")
    except:
        if verbose: print('''provide headwater_keys, down_connections, and a terminal code
to print Downstream Connections.

Provide terminal_keys, up_connections, down_connections, and a terminal code
to print Upstream Connections.''')

if 1 == 1:
    """##TEST"""
    print("")
    print ('Executing Test')
    # Test data
    test_rows = [
        [0,456,-999,0],
        [1,178,4,0],
        [2,394,0,0],
        [3,301,2,0],
        [4,798,0,0],
        [5,679,4,0],
        [6,523,0,0],
        [7,815,2,0],
        [8,841,-999,0],
        [9,514,12,0],
        [10,458,9,0],
        [11,832,8,0],
        [12,543,8,0],
        [13,240,14,0],
        [14,548,10,0],
        [15,920,14,0],
    ]

    test_key_col = 0
    test_downstream_col = 2
    test_length_col = 1
    test_terminal_code = -999

    (test_all_keys, test_ref_keys, test_headwater_keys
     , test_terminal_keys) = determine_keys(
                 rows = test_rows
                 , key_col = test_key_col
                 , downstream_col = test_downstream_col
                 , terminal_code = test_terminal_code
                 , verbose = True
                 , debuglevel = -2)

    (test_down_connections
     , test_up_connections) = build_connections(
                 rows = test_rows
                 , key_col = test_key_col
                 , downstream_col = test_downstream_col
                 , length_col = test_length_col
                 , terminal_code = test_terminal_code
                 , headwater_keys = test_headwater_keys
                 , terminal_keys = test_terminal_keys
                 , verbose = True
                 , debuglevel = -2)

    print_connections(headwater_keys = test_headwater_keys
                    , terminal_keys = test_terminal_keys
                    , down_connections = test_down_connections
                    , up_connections = test_up_connections
                    , terminal_code = test_terminal_code)


if 1 == 1:
    """##NHD Subset (Brazos/Lower Colorado)"""
    import sys
    import os
    import geopandas as gpd
    # import numpy as np

    # root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # test_folder = os.path.join(root, r'test')
    # input_folder = os.path.join(test_folder, r'input', r'geo')
    # input_path = os.path.join(input_folder, r'input.txt')
    # nhd_conus = gpd.read_file(os.path.join('..','test','input','geo','Channels','NHD_BrazosLowerColorado_Channels.shp'))
    # nhd_conus = gpd.read_file('/content/small/trunk/NDHMS/dynamic_channel_routing/test/input/text/Channels/NHD_BrazosLowerColorado_Channels.shp')
    # nhd_conus = gpd.read_file('/content/small/trunk/NDHMS/dynamic_channel_routing/test/input/text/Channels/Channels.shp')

    CONUS = False
    if CONUS:
        nhd_conus = gpd.read_file('../test/input/geo/Channels/NHD_Conus_Channels.shp')
        key_col_NHD = 1
        downstream_col_NHD = 6
        length_col_NHD = 5
        terminal_code_NHD = 0

    else:
        nhd_conus = gpd.read_file('../test/input/geo/Channels/NHD_BrazosLowerColorado_Channels.shp')
        key_col_NHD = 2
        downstream_col_NHD = 7
        length_col_NHD = 6
        terminal_code_NHD = 0

    nhd_conus_rows = nhd_conus.to_numpy()

    # Kick off recursive call for all connections and keys
    (all_keys_NHD, ref_keys_NHD, headwater_keys_NHD
     , terminal_keys_NHD) = determine_keys(
                 rows = nhd_conus_rows
                 , key_col = key_col_NHD
                 , downstream_col = downstream_col_NHD
                 , terminal_code = terminal_code_NHD
                 , verbose = True
                 , debuglevel = 0)

    (down_connections_NHD
     , up_connections_NHD) = build_connections(
                 rows = nhd_conus_rows
                 , key_col = key_col_NHD
                 , downstream_col = downstream_col_NHD
                 , length_col = length_col_NHD
                 , terminal_code = terminal_code_NHD
                 , headwater_keys = headwater_keys_NHD
                 , terminal_keys = terminal_keys_NHD
                 , verbose = True
                 , debuglevel = 0)

# print_connections(headwater_keys = test_headwater_keys
#                 , terminal_keys = test_terminal_keys
#                 , down_connections = test_down_connections
#                 , up_connections = test_up_connections
#                 , terminal_code = test_terminal_code)

    for key, value in up_connections_NHD.items():
        if len(value['upstreams']) > 1:
        # if 1 == 1:
            # print (link, link['upstreams'][:])
            print (key, value['upstreams'])


    print(len(down_connections_NHD))
    print(len(up_connections_NHD))