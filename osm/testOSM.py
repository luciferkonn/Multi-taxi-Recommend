# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 14:35:29 2017

@author: apola
"""

#from IPython import get_ipython
#get_ipython().magic('reset -sf')


from spatialite_osm_node_find import *


# Global variables
passanger_capacity = 4  # maximum count of passenger that can travel in one way
route_dict = dict()  # Global dictionary to keep the routing distance between previously discovered nodes
osm_file = './data/NewYork.osm'
db_name = './data/new_york_cost.sqlite'

virtual_network_table_name = 'roads_nodes'
osm_id, node_id =  'osm_id', 'node_id'
time_format = '%Y-%m-%d %H:%M:%S'

# data has the city graph
data = spatialite_osm_node_finder(osm_file, db_name,virtual_network_table_name , osm_id, node_id )

# Establish db connection
db = sqlite3.connect(db_name)
db.enable_load_extension(True)
db.load_extension('/usr/local/lib/mod_spatialite')
cur = db.cursor()


def route_distance_node_id(from_node_id, to_node_id):
# route_query = "SELECT ST_Length(geometry) AS length FROM roads_net WHERE NodeFrom=%s AND NodeTo=%s;" % (from_node_id, to_node_id)
    route_query = "SELECT * FROM roads_net WHERE NodeFrom=%s AND NodeTo=%s;" % (from_node_id, to_node_id)
    tmpq_data = cur.execute(route_query)
    tmp_list = []
    for i in tmpq_data:
        tmp_list.append((i[2],i[3],i[4]))
    # printing when successful
    if tmp_list:
        return tmp_list
    else:
        return float('-inf')


# from_node_id = data.find_grid_point_node_id(float(row[11]), float(row[10]))
# to_node_id = data.find_grid_point_node_id(float(row[13]), float(row[12]))
from_node_id = data.find_grid_point_node_id(float(40.781887), float(-73.955925))
to_node_id = data.find_grid_point_node_id(float(40.777832), float(-73.963181))

m_path_list = route_distance_node_id(from_node_id, to_node_id)

print(m_path_list)
