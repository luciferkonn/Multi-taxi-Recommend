"""
@author: Jikun Kang
"""
import math
from osm_grid import *
import numpy as np
import decimal
import time
import csv

# Global variables
osm_file = './data/NewYork.osm'
# db_name = './data/sorted_by_week/nyData_Monday.sqlite'
table_name = 'my_table'
osm_id, node_id = 'osm_id', 'node_id'
time_format = '%Y-%m-%d %H:%M:%S'

# lonMin, lonMax, latMin, latMax get from OSM files
LONMIN = -74.36
LONMAX = -73.67001
LATMIN = 40.48
LATMAX = 40.95999
GRID_X = 100
GRID_Y = 100
grid_size = 100

passenger_number = np.zeros((100, 100))
taxi_number = np.zeros((100, 100))

longitude_interval = (LONMAX - LONMIN) / GRID_X
latitude_interval = (LATMAX - LATMIN) / GRID_Y


def get_num_lon(lon):
    if isinstance(lon, unicode):
        return 101
    return abs(int(math.floor((lon - LONMIN) / longitude_interval)))


def get_num_lat(lat):
    if isinstance(lat, unicode):
        return 101
    return abs(int(math.floor((lat - LATMIN) / latitude_interval)))


def get_Hour(date):
    return time.strptime(date, '%Y-%m-%d %H:%M:%S').tm_hour


db_name = '../../data/sorted_by_week/nyData_Monday.sqlite'
try:
    db = sqlite3.connect(db_name)
    db.enable_load_extension(True)
    db.load_extension('/usr/local/lib/mod_spatialite')
    cur = db.cursor()
    sql = 'select dist, travel_time from ' + table_name
    # sql = 'select * from ' + table_name
except Exception as err:
    print("Error" + str(err))

# define distance and travel time
dist = 0
travel_time = 0
for row in cur.execute(sql):
    if row is not None and row[0] is not None and row[1] is not None:
        # dist += int(row[0])
        print(row[1])
        # travel_time += int(row[1])

# print(dist)
# print(travel_time)
