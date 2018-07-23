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
db_name = './data/sorted_by_week/nyData_Monday.sqlite'
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

# data has the city graph
# data = spatialite_osm_node_finder(osm_file, db_name, table_name, osm_id, node_id)

# grid the map using square policy
# passenger_number = np.zeros((100, 100, 24))
# taxi_number = np.zeros((100, 100, 24))
# pr = np.zeros((100, 100, 24))
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


# for num in range(1, 366):
#     db_name = './data/sorted_by_day/nyData_Monday_'+str(num)+'.sqlite'
#     try:
#         f = open(db_name)
#     except IOError as e:
#         continue
#     try:
#         db = sqlite3.connect(db_name)
#         db.load_extension('/usr/local/lib/mod_spatialite')
#         cur = db.cursor()
#         sql = 'select pickup_lon, pickup_lat, drop_lon, drop_lat, pickup_time, drop_time from ' + table_name
#     except Exception as err:
#         print("Error" + str(err))
#     for row in cur.execute(sql):
#         if row is not None and row[1] is not None and row[2] is not None and row[3] is not None and row[0] is not None and row[4] is not None and row[5] is not None:
#             x_axis = get_num_lat(row[1])
#             y_axis = get_num_lon(row[0])
#             z_axis = get_Hour(row[4])  # z_axis refers to pickup time axis
#             a_axis = get_num_lat(row[3])
#             b_axis = get_num_lon(row[2])
#             c_axis = get_Hour(row[5])  # c_axis refers to drop time axis
#             # print(x_axis,y_axis,a_axis,b_axis)
#             if x_axis >= 100 or y_axis >= 100 or a_axis >= 100 or b_axis >= 100:
#                 continue
#             passenger_number[x_axis][y_axis][z_axis] += 1
#             taxi_number[a_axis][b_axis][c_axis] += 1
#
#     # output passenger request to file
#     out_pas = open('./data/probability/Monday_passenger_request'+str(num), 'w')
#     for i in range(100):
#         for j in range(100):
#             for k in range(24):
#                 if passenger_number[i][j][k] != 0:
#                     # print('[' + str(i) + ']' + '[' + str(j) + ']:' + str(passenger_number[i][j]) )
#                     print >> out_pas, "[%d][%d][%d]: %d" % (i, j, k, passenger_number[i][j][k])
#     out_pas.close()
#     out_taxi = open('./data/probability/Monday_taxi_available'+str(num), 'w')
#     for i in range(100):
#         for j in range(100):
#             for k in range(24):
#                 if taxi_number[i][j][k] != 0:
#                     # print('[' + str(i) + ']' + '[' + str(j) + ']:' + str(taxi_number[i][j]) )
#                     print >> out_taxi, "[%d][%d][%d]: %d" % (i, j, k, taxi_number[i][j][k])
#     out_taxi.close()
#
#     out_pr = open('./data/probability/Monday_pickup_pr'+str(num), 'w')
#     for i in range(100):
#         for j in range(100):
#             for k in range(24):
#                 if passenger_number[i][j][k] > 0 and taxi_number[i][j][k] > 0:
#                     # pr[i][j] = passenger_number/taxi_number
#                     print >> out_pr, "[%d][%d][%d]: %f" % (i, j, k, passenger_number[i][j][k] / taxi_number[i][j][k])
#     out_pr.close()
# Establish db connection
db_name = '../../data/sorted_by_week/nyData_Sunday.sqlite'
try:
    db = sqlite3.connect(db_name)
    db.enable_load_extension(True)
    db.load_extension('/usr/local/lib/mod_spatialite')
    cur = db.cursor()
    sql = 'select pickup_lon, pickup_lat, drop_lon, drop_lat from ' + table_name
    # sql = 'select * from ' + table_name
except Exception as err:
    print("Error" + str(err))
for row in cur.execute(sql):
    if row is not None and row[1] is not None and row[2] is not None and row[3] is not None and row[0] is not None:
        x_axis = get_num_lat(row[1])
        y_axis = get_num_lon(row[0])
        a_axis = get_num_lat(row[3])
        b_axis = get_num_lon(row[2])
        # print(x_axis,y_axis,a_axis,b_axis)
        if x_axis>=100 or y_axis>=100 or a_axis>=100 or b_axis>=100:
            continue
        passenger_number[x_axis][y_axis] += 1
        taxi_number[a_axis][b_axis] += 1

# output passenger request to file
out_pas = open('../../data/passenger_request_Sunday', 'w')
for i in range(100):
    for j in range(100):
        if passenger_number[i][j] != 0:
            # print('[' + str(i) + ']' + '[' + str(j) + ']:' + str(passenger_number[i][j]) )
            print >> out_pas, "%d,%d,%d" %(i, j , passenger_number[i][j])
out_pas.close()
out_taxi = open('../../data/taxi_available_Sunday', 'w')
for i in range(100):
    for j in range(100):
        if taxi_number[i][j] != 0:
            # print('[' + str(i) + ']' + '[' + str(j) + ']:' + str(taxi_number[i][j]) )
            print >> out_taxi, "%d,%d,%d" %(i, j , taxi_number[i][j])
out_taxi.close()

out_pr = open('../../data/pickup_pr_Sunday', 'w')
for i in range(100):
    for j in range(100):
        if passenger_number[i][j] > 0 and taxi_number[i][j] > 0:
            # print('[' + str(i) + ']' + '[' + str(j) + ']:' + str(taxi_number[i][j]) )
            print >> out_pr, "%d,%d,%f" %(i, j , passenger_number[i][j]/taxi_number[i][j])
out_pr.close()

# find_pr = np.zeros((grid_size, grid_size))
# # out_pr = open('../../data/pickup_pr', 'w')
# for i in range(100):
#     for j in range(100):
#         if passenger_number[i][j] > 0 and taxi_number[i][j] > 0:
#             # pr[i][j] = passenger_number/taxi_number
#             find_pr[i][j] = passenger_number[i][j]/taxi_number[i][j]
#             # print >> out_pr, "[%d][%d]: %f" %(i, j , passenger_number[i][j]/taxi_number[i][j])
# print(find_pr)
# with open('../../data/pickup_pr_csv', 'wb') as csvfile:
#     matrixwriter = csv.writer(csvfile, delimiter=' ')
#     for row in find_pr:
#         matrixwriter.writerow(row)
#
#
# def get_pr():
#     return find_pr