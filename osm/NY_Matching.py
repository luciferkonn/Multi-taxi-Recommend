# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 22:31:35 2016

@author: apola
"""
# from IPython import get_ipython
# ipython = get_ipython()
# ipython.magic('reset -sf')

# for file looping
import os
import csv
import time
import random
from uuid import getnode as get_mac
## for matching
import networkx as nx
from datetime import datetime
import sqlite3
from spatialite_osm_node_find import *

## Global variables
passanger_capacity = 4  # maximum count of passenger that can travel in one way
route_dict = dict()  # Global dictionary to keep the routing distance between previously discovered nodes
osm_file = '/home/lucifer/Documents/PycharmProjects/data/NewYork.osm'
db_name = '/home/lucifer/Documents/PycharmProjects/data/new_york_cost.sqlite'

virtual_network_table_name = 'roads_nodes'
osm_id, node_id = 'osm_id', 'node_id'
time_format = '%Y-%m-%d %H:%M:%S'

# data has the city graph
data = spatialite_osm_node_finder(osm_file, db_name, virtual_network_table_name, osm_id, node_id)

# Establish db connection
db = sqlite3.connect(db_name)
db.enable_load_extension(True)
db.load_extension('/usr/local/lib/mod_spatialite')
cur = db.cursor()


def Get_required_V():
    ##
    m_file_list_dir = os.path.abspath('processed/file_list.csv')
    m_file_list_name = list()
    with open(m_file_list_dir, 'rb') as csvfile:
        rowspam = csv.reader(csvfile, delimiter=',')
        for i in rowspam:
            m_file_list_name.append(i[0])

    m_processed_list_dir = os.path.abspath('processed/24hr_processed_list.csv')
    if (not os.path.isfile(m_processed_list_dir)):
        with open(m_processed_list_dir, 'a') as csvfile:
            rowWspam = csv.writer(csvfile, delimiter=',')
            rowWspam.writerow(['File created', get_mac(), time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())])

    m_cnt_processed = 0
    with open(m_processed_list_dir, 'a+') as csvfile:
        rowspam = csv.reader(csvfile, delimiter=',')
        for i in rowspam:
            m_cnt_processed += 1
        m_ready_to_processed = m_file_list_name[m_cnt_processed - 1]
        rowWspam = csv.writer(csvfile, delimiter=',')
        rowWspam.writerow([m_ready_to_processed, get_mac(), time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())])

    # check deluse dir is existed or not, if not, create dir
    m_subsample_dir = os.path.abspath('processed/' + m_ready_to_processed[0:8] + '/5min_24hr')
    m_is_dir_exist = os.path.isdir(m_subsample_dir)
    if (not m_is_dir_exist):
        os.makedirs(m_subsample_dir)

    print 'File is generated at: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

    return m_ready_to_processed, m_subsample_dir, m_cnt_processed


########################################################################################################################
# Input: - node ids n1, n2, n3 and n4
# Output: - distance
# function: finds the shortest possible route distance between n1-->n2-->n3-->n4 #
########################################################################################################################
def find_route_distance(n1, n2, n3, n4):
    distance = 0  # cumulutive distance
    # 1. n1 --> n2 # find the dicatance between points n1 and n2
    if (
    n1, n2) in route_dict:  # if the distance has already been discovered, take it from route dictionary i.e. route_dict
        distance = route_dict[(n1, n2)]
    else:
        try:
            d = route_distance_node_id(n1, n2)  # find the distance between two points using routing function
            if d != None:
                distance = distance + d
                route_dict[(n2, n3)] = d  # update the new distance between two points in the route_dict
        except:
            return float("inf")
    # 2. n2 --> n3
    if (n2, n3) in route_dict:
        distance = distance + route_dict[(n2, n3)]
    else:
        try:
            d = route_distance_node_id(n2, n3)
            if d != None:
                distance = distance + d
                route_dict[(n2, n3)] = d
        except:
            return float("inf")
    # 3, n3 --> n4
    if (n3, n4) in route_dict:
        distance = distance + route_dict[(n3, n4)]
    else:
        try:
            d = route_distance_node_id(n3, n4)
            if d != None:
                distance = distance + d
                route_dict[(n2, n3)] = d
        except:
            return float("inf")
    return distance


########################################################################################################################
# Input: - nodes of graph "G", i.e. nodes with passanger details
# Output: - distance
# function: finds the shortest possible route between two passanger #
########################################################################################################################
def find_min_route_dist(p1, p2):
    s1 = G.node[p1]['source']  # source of the first trip
    d1 = G.node[p1]['destination']  # destination of the first trip
    s2 = G.node[p2]['source']  # source of the second trip
    d2 = G.node[p2]['destination']  # destination of the second trip
    # four possible ways of combining the routes:
    # 1. s1,s2,d1,d2
    distance_1 = find_route_distance(s1, s2, d1, d2)
    # 2. s1,s2,d2,d1
    distance_2 = find_route_distance(s1, s2, d2, d1)
    # 3. s2,s1,d1,d2
    distance_3 = find_route_distance(s2, s1, d1, d2)
    # 4. s2,s1,d2,d1
    distance_4 = find_route_distance(s2, s1, d2, d1)
    # return the minimum distance from all possible route
    return min(distance_4, distance_3, distance_2, distance_1)


#################################################################
# Input: - node ids of two points: from_node_id and to_node_id          #
# Output: - routing distance between two points                         #
# function: based on spatialite routing return the shortest path distance between "from_node_id" to "to_node_id"
#
#################################################################
# find distance between given two node ids using the spatialite database
def route_distance_node_id(from_node_id, to_node_id):
    #    route_query = "SELECT ST_Length(geometry) AS length FROM roads_net WHERE NodeFrom=%s AND NodeTo=%s;" % (from_node_id, to_node_id)
    route_query = "SELECT * FROM roads_net WHERE NodeFrom=%s AND NodeTo=%s;" % (from_node_id, to_node_id)
    cur.execute(route_query)
    route = cur.fetchone()
    # printing when successful
    if route != None:
        return route[4] / 1000
    else:
        return float('-inf')


#################################################################
# Input: - start GPS and end GPS of two taxi data           #
# Output: - whether the geometry of two route overlap, True or False                        #
# function: based on math geometry
#
#################################################################
# find distance between given two node ids using the spatialite database
def overlap_check(from_lat1, from_lon1, to_lat1, to_lon1, from_lat2, from_lon2, to_lat2, to_lon2):
    # if temp is negative, it means the point is in between
    # for first route in lat direction
    temp1 = (from_lat1 - from_lat2) * (from_lat1 - to_lat2)
    temp2 = (to_lat1 - from_lat2) * (to_lat1 - to_lat2)
    # for second route in lat direction
    temp3 = (from_lat2 - from_lat1) * (from_lat2 - to_lat1)
    temp4 = (to_lat2 - from_lat1) * (to_lat2 - to_lat1)
    if (temp1 or temp2 or temp3 or temp4):
        return True

    # for first route in lon direction
    temp1 = (from_lon1 - from_lon2) * (from_lon1 - to_lon2)
    temp2 = (to_lon1 - from_lon2) * (to_lon1 - to_lon2)
    # for second route in lon direction
    temp3 = (from_lon2 - from_lon1) * (from_lon2 - to_lon1)
    temp4 = (to_lon2 - from_lon1) * (to_lon2 - to_lon1)
    if (temp1 or temp2 or temp3 or temp4):
        return True
    # no overlap at all
    return False


#####################################
#    check if the input string is number, since the data set is dirty, sometimes it contains empty string in LatLng column
#####################################
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


################################################################################################################
#           Start creating the graph                                                                           #
################################################################################################################
## start creating graph
# %%
m_cnt_processed = 0
while (m_cnt_processed < 365):
    # for i in range(1):
    # Load data
    start_timer = time.time()
    m_ready_to_processed, m_subsample_dir, m_cnt_processed = Get_required_V()

    #    m_ready_to_processed = '13_02_09_sorted.csv'
    #    m_subsample_dir = 'processed/'+m_ready_to_processed[0:8]+'/5min_8hr'

    stop_time = datetime.strptime('20' + m_ready_to_processed[0:8] + ' 23:59:59', '%Y_%m_%d %H:%M:%S')
    taxi_file_name = os.path.abspath('/home/lucifer/Documents/PycharmProjects/data/original/' + m_ready_to_processed)
    key = 0  # key is the id of individual node
    count = 0  # a temporary variable
    G = nx.Graph()  # the connected graph between all the passangers
    time_interval = 5  # max time difference between start times of two independent passangers
    not_found = []  # a list of (lat,lan) not found in our graph, for analysis purpose, can be safely removed
    found_node = []  # a list of (lat,lan) FOUND by our code, for analysis purpose, can be safely removed
    number_of_node_not_found = 0  # a counter for total number of node not found so far

    c = 0
    pr_time = 0
    # start creating the graph from the taxi data, IT assumes taxi_file_name to be sorted:
    with open(taxi_file_name, 'rb') as csvfile:
        # open the csv.reader
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if (c % 50 == 0):
                print 'Processing ' + row[5][0:20] + "  ----->count is : " + str(c) + "  ------>time taken :" + str(
                    time.time() - pr_time)[0:4]
                pr_time = time.time()
            c = c + 1
            # check if the date format is correct
            try:
                trip_start_time = datetime.strptime(row[5][0:20], time_format)
            except ValueError:
                not_found.append([(float(row[11]), float(row[10])), (float(row[13]), float(row[12]))])
                continue

            if trip_start_time > stop_time:
                # time to stop the loop
                break
            # check if lng lat can be parse without problem
            if (not (is_number(row[10]) and is_number(row[11]) and is_number(row[12]) and is_number(row[13]))):
                continue
            # find the corresponding osm id based on latitude and longitude
            from_node_id = data.find_grid_point_node_id(float(row[11]), float(row[10]))
            to_node_id = data.find_grid_point_node_id(float(row[13]), float(row[12]))
            if from_node_id is None or to_node_id is None:  # cannot find the node by find_grid_point_node_id()
                not_found.append([(float(row[11]), float(row[10])), (float(row[13]), float(row[12]))])
                # not_found.append([(float(row[0]), float(row[1])), (float(row[2]), float(row[3]))])
                number_of_node_not_found = number_of_node_not_found + 1
                # print "source or destination cannot find. passing."
                continue  # ignore this row and continue!
            else:
                # calculate the distance between the start and end of the node!!
                distance = data.route_distance_node_id(from_node_id, to_node_id)
                if distance != float("inf") and distance != None and distance != float("-inf") and distance > 0:
                    key = key + 1
                    G.add_node(key, source=from_node_id, destination=to_node_id,
                               distance=distance, start_time=trip_start_time, passanger_count=int(row[7]),
                               from_lat=float(row[11]), from_lon=float(row[10]), to_lat=float(row[13]),
                               to_lon=float(row[12]))
                else:  # there is no link between source and destination
                    continue
            # ADD EDGES based on previously added nodes:
            start_key = key - 1;  # Start adding kth node with nodes (k-1) .. 1
            i = 0
            ################################################################################################################
            # PROBLEM IS HERE: Creating edges between multiple nodes needs finding multiple routes, and finding route is time consuming task,
            # Hence the below code takes an unusual amount of time!!
            ################################################################################################################
            while key > 1 and (key - i) > 1:  # this loop only breaks after time interval is not matched
                # print "ADDING EDGES: " + str(key) + " and " + str(key - i - 1)
                i = i + 1
                # if time difference between two routes is less than specified then continue adding it
                time_difference = abs(G.node[key]['start_time'] - G.node[key - i]['start_time'])
                if time_difference.days == 0 and time_difference.seconds / 60 <= time_interval:
                    # TODO : USE HEURISTICS TO OPTIMIZE THE NUMBER OF CALLS
                    overlap_check_val = overlap_check(G.node[key]['from_lat'], G.node[key]['from_lon'],
                                                      G.node[key]['to_lat'], G.node[key]['to_lon'],
                                                      G.node[key - i]['from_lat'], G.node[key - i]['from_lon'],
                                                      G.node[key - i]['to_lat'], G.node[key - i]['to_lon'])
                    #                overlap_check_val=True
                    if G.node[key]['passanger_count'] + G.node[key - i][
                        'passanger_count'] < passanger_capacity and overlap_check_val:  # passanger capacity should not more than cab capacity
                        # calculate the minimum cost of a route
                        min_route_distance = find_min_route_dist(key, key - i)
                        # check overlap
                        # Decide if two nodes should be connected on basis of distance
                        if ((G.node[key]['distance'] + G.node[key - i]['distance']) > min_route_distance):
                            selected_route_distance = G.node[key]['distance'] + G.node[key - i][
                                'distance'] - min_route_distance

                            #                        if not (math.isnan(uti_s1_v1) or math.isnan(uti_s1_v2) or math.isinf(uti_s1_v1) or math.isinf(uti_s1_v2) or uti_s1_v1 < 0 or uti_s1_v2 < 0):
                            G.add_weighted_edges_from([(key, key - i, selected_route_distance)])
                #                                                       ,u1=uti_s1_v1,v1=uti_s1_v2, u2=uti_s2_v1,v2=uti_s2_v2,
                #                                                       u3=uti_s3_v1,v3=uti_s3_v2, u4=uti_s4_v1,v4=uti_s4_v2)
                # nx.get_edge_attributes(G,'u')
                # print "edge added"+ str(key) + "and"+ str(key - i)
                else:
                    break
                    print "Time Difference reached"
            # print "Added Node " + str(key)

    time_taken = time.time() - start_timer
    print("--- Time taken to pair the passengers: %s seconds " % (time.time() - start_timer))

    # %%
    result_file = m_subsample_dir + '/node.csv'
    # result_file = "test_resutl.csv"

    with open(result_file, 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerow(['key', 'from_node_id', 'to_node_id', 'distance', 'start_time', 'passanger_count'])
        for e in G.nodes():
            a.writerow([e, G.node[e]['source'], G.node[e]['destination'], G.node[e]['distance'],
                        G.node[e]['start_time'], G.node[e]['passanger_count']])

    result_file = m_subsample_dir + '/edge.csv'
    with open(result_file, 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerow(['from', 'to', 'weight'])
        for e in G.nodes():
            if G.neighbors(e):
                m_tmp_ind = sorted(G.neighbors(e))
                for e_ in m_tmp_ind:
                    a.writerow([e, e_, "{:3.6f}".format(G.get_edge_data(*(e, e_))['weight'])])
    G.clear()