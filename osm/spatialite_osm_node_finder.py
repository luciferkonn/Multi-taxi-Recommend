########################################################################################################
# FILE NAME:            spatialite_osm_node_finder.py.
# FILE FUNCTION:        Loads the OSM (Open Street Maps) data of the city.
# AUTHOR:               Mukesh Jha.
# PROBLEM:              ??? Perhaps there is no problem in this file, the problem is in the other one.
# EDITOR:               Abdullah Heyari.
# PROJECT SUPERVISOR:   Prof. Sid Chi-Kin Chau.
# PROJECT DURATION:     November 2015 - 31st December 2015.
# INSTITUTE:            Masdar Institute of Science and Technology, Abu Dhabi, UAE.
########################################################################################################

import os
from xml.sax import make_parser, handler
import xml
from haversine import haversine
import sqlite3


############## Variables
### input variables
# filename : name of the osm file, which we are going to consider for the city
# db_name : the spatialite database for the city
# table_name : the routing table corresponding to the road network in the database
# osm_id_column : Name of the osm column (based in osm file) in the  road network table
# node_id_column : Name of the node id (based in database) in the  road network table
# grid_x : the x division of the map, default value 100
# grid_y : the y division of the map, default value 100
####
#### class variables
#        self.all_nodes : dictionary of all the nodes present in the osm file
#        self.nodes     : the nodes on road, which are relevent for us
#        self.latMin    : the minimum possible latitude in the given map
#        self.latMax    : the maximum possible latitude in the given map
#        self.lonMin    : the minimum possible longitude in the given map
#        self.lonMax    : the maximum possible longitude in the given map
#        self.loadOsm(filename) : load the osm file given
#        self.gridDictionary : list of dictionary of grids, each grid is collection of osm nodes in that grid
#        self.latitude_list : the list of longitude intervals in the grid
#        self.longitude_list  : the list of latitude intervals in the grid
#        self.grid_x : same as grid_x
#        self.grid_y  : same as grid_y
#        self.osm_id_node_id : dictionary to correspond between osm_id (osm file) and node_id (database)
#        self.db_name : the given database
#        self.table_name : name of table given
#        self.osm_id_column  : Name of the osm column (based in osm file) in the  road network table
#        self.node_id_column :  Name of the node id (based in database) in the  road network table
#        self.db_connection  :
#        self.cur : to execute database query
#        self.createGrid : function to create the grid of the osm nodes
##################################################################################################################


class spatialite_osm_node_finder(handler.ContentHandler):
    def __init__(self, filename, db_name, table_name, osm_id_column, node_id_column, grid_x=100, grid_y=100):
        self.all_nodes = {}
        self.nodes = {}
        self.latMin = float("inf")
        self.latMax = float("-inf")
        self.lonMin = float("inf")
        self.lonMax = float("-inf")
        self.loadOsm(filename)
        self.gridDictionary = []  # list of dictionary
        self.latitude_list = 0
        self.longitude_list = 0
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.osm_id_node_id = {}  ##
        self.db_name = db_name
        self.table_name = table_name
        self.osm_id_column = osm_id_column
        self.node_id_column = node_id_column
        self.db_connection = None
        self.cur = None
        self.createGrid()

    #        self.remove_unwanted_variables()
    #################################################################
    # Input:
    # Output:
    # function: connects to the given spatialite database
    #################################################################
    def connect_to_database(self):
        try:
            self.db_connection = sqlite3.connect(self.db_name)
            self.db_connection.enable_load_extension(True)
            self.db_connection.load_extension('libspatialite')
            self.cur = self.db_connection.cursor()
        except Exception, e:
            print("Unable to create connection, Exception:  %s", str(e))
            return e

    #################################################################
    # Input: -                          #
    # Output: -                         #
    # function: safely closes the database connection       #
    #################################################################

    def close_db_connection(self):
        try:
            self.db_connection.close()
            self.cur.close()
        except Exception, e:
            print("Unable to close connection, Exception:  %s", str(e))
            return e

    ######################################################################
    # Input:
    # Output:
    # function: remove the unwanted class variable once the map is loaded
    ######################################################################

    def remove_unwanted_variables(self):
        del self.all_nodes

    #################################################################
    # Input:
    # Output:
    # function: parse and load the osm file
    #################################################################

    def loadOsm(self, filename):
        if (not os.path.exists(filename)):
            print "No such data file %s" % filename
            return
        try:
            parser = make_parser()
            parser.setContentHandler(self)
            parser.parse(filename)
        except xml.sax._exceptions.SAXParseException:
            print "Error loading %s" % filename

    def startElement(self, name, attrs):
        if name in ('node', 'way'):
            if name == 'node':
                # """Nodes need to be stored"""
                id = int(attrs.get('id'))
                lat = float(attrs.get('lat'))
                lon = float(attrs.get('lon'))
                # min latitude
                if lat < self.latMin:
                    self.latMin = lat
                # max latitude
                if lat > self.latMax:
                    self.latMax = lat
                # min longitude
                if lon < self.lonMin:
                    self.lonMin = lon
                # max longitude
                if lon > self.lonMax:
                    self.lonMax = lon
                # store node
                self.all_nodes[id] = (lat, lon)

    #################################################################
    # Input:    coordinates as a tuple of latitude and longitude
    # Output:   return either None or valid grid number
    # function: find corresponding grid for a given coordinates
    #################################################################

    def find_grid(self, coordinates):
        latitude = coordinates[0]
        longitude = coordinates[1]
        search_latitude_grid = -1
        search_longitude_grid = -1
        # if given co-ordinate is out of our grid system i.e. self.latitude_list[0] is infact self.latMin..
        if longitude < self.longitude_list[0] or longitude > self.longitude_list[-1]:
            return None
        ##   if given co-ordinate is out of our grid system
        if latitude < self.latitude_list[0] or latitude > self.latitude_list[-1]:
            return None
        ## start finding the grid longitude
        for i in range(len(self.longitude_list) - 1):
            if (self.longitude_list[i] <= longitude and longitude <= self.longitude_list[i + 1]):
                search_longitude_grid = i
                break
        ## start finding the grid latitude
        for i in range(len(self.latitude_list) - 1):
            if (self.latitude_list[i] <= latitude and latitude <= self.latitude_list[i + 1]):
                search_latitude_grid = i
                break
        ## check if the grid found was correct
        if search_latitude_grid == -1 or search_longitude_grid == -1:
            return None
        else:
            return (search_latitude_grid + self.grid_x * search_longitude_grid)

    #################################################################
    # Input:
    # Output:   PROCEDURE
    # function: create the grid of given map
    #################################################################

    def createGrid(self):
        self.gridDictionary = [dict() for x in range(self.grid_x * self.grid_y)]
        latitude_interval = (self.latMax - self.latMin) / self.grid_x
        longitude_interval = (self.lonMax - self.lonMin) / self.grid_y
        self.latitude_list = [latitude_interval * i + self.latMin for i in range(0, self.grid_x)]
        self.latitude_list.append(self.latMax)
        self.longitude_list = [longitude_interval * i + self.lonMin for i in range(0, self.grid_y)]
        self.longitude_list.append(self.lonMax)
        ## connect to db
        try:
            self.connect_to_database()
        except Exception, e:
            print("unable to connect to database, please provide db name with full path : Error: ", str(e))
            return
        ## read the table and create the grid dictionay accordingly
        try:
            sql_query = "select " + self.osm_id_column + " , " + self.node_id_column + "  " + " from " + self.table_name + ";"
            for row in self.cur.execute(sql_query):
                if row is not None:
                    osm_id = row[0]
                    node_id = row[1]
                    self.osm_id_node_id[osm_id] = node_id
                    if osm_id in self.all_nodes:
                        self.nodes[osm_id] = self.all_nodes[osm_id]
                        gridNumber = self.find_grid(self.nodes[osm_id])
                        if gridNumber != None:
                            self.gridDictionary[gridNumber][osm_id] = self.nodes[osm_id]
            ## Close cursor after the operaion
            # self.close_db_connection()
        except:
            print("Please check the table name and row name provided in parameters")
            return

    #####################################################################
    # Input:    latutude, longitude, ThresholdMinDist
    # Output:   node id based on spatialite database
    # function: return a "node id" within the ThresholdMinDist distance
    #####################################################################

    def find_grid_point_node_id(self, latitude, longitude,
                                ThresholdMinDist=0.010):  # consider the node found if it's in range of 100 meter range
        maxDist = 1000
        # for efficiency, if a node is closer
        nodeFound = None
        grid_number = self.find_grid((latitude, longitude))
        if grid_number == None:
            # print "Could not find id"
            return None
        else:
            for id in self.gridDictionary[grid_number].keys():
                if id not in self.nodes:
                    # print "Ignoring undefined node %s" % id
                    continue
                n = self.nodes[id]
                dist = haversine([n[0], n[1]], [latitude, longitude])  # in kilometers
                if dist < maxDist:
                    maxDist = dist
                    nodeFound = id
                # Optimization, if the node is withing threshold, we can return it
                if dist <= ThresholdMinDist:
                    nodeFound = id
                    # print "from Threshold"
                    # return(nodeFound)
                    return self.osm_id_node_id[nodeFound]
        if nodeFound != None:
            return (self.osm_id_node_id[nodeFound])
        else:
            return None

    ########################################################################################################
    # Input:    latitude, longitude, ThresholdMinDist
    # Output:   osm id based on osm file
    # function: return a "osm id" within the ThresholdMinDist distance of the given latitude and longitude
    ########################################################################################################

    def find_grid_point_osm_id(self, latitude, longitude,
                               ThresholdMinDist=0.010):  # consider the node found if it's in range of 100 meter range
        maxDist = 1000
        # for efficiency, if a node is closer
        nodeFound = None
        grid_number = self.find_grid((latitude, longitude))
        if grid_number == None:
            # print "Could not find id"
            return None
        else:
            for id in self.gridDictionary[grid_number].keys():
                if id not in self.nodes:
                    # print "Ignoring undefined node %s" % id
                    continue
                n = self.nodes[id]
                dist = haversine([n[0], n[1]], [latitude, longitude])  # in kilometers
                if dist < maxDist:
                    maxDist = dist
                    nodeFound = id
                # Optimization, if the node is withing threshold, we can return it
                if dist <= ThresholdMinDist:
                    nodeFound = id
                    # print "from Threshold"
                    # return(nodeFound)
                    return nodeFound
        if nodeFound != None:
            return nodeFound
        else:
            return None

    #############################################################################################
    # Input: - latitude, longitude of the two points (lat1, lon1) and (lat2, lon2)
    # Output: - routing distance between two points
    # function: based on spatialite routing return the shortest path distance between two points
    #############################################################################################

    def distance_between_two_points(self, lat1, lon1, lat2, lon2):
        from_node_id = self.find_grid_point_node_id(lat1, lon1)
        to_node_id = self.find_grid_point_node_id(lat2, lon2)
        if from_node_id != None and to_node_id != None:
            distance_query = "SELECT  ST_Length(geometry) AS lenght FROM roads_net WHERE NodeFrom=%s AND NodeTo=%s;" % (
            from_node_id, to_node_id)
            self.cur.execute(distance_query)
            route = self.cur.fetchone()
            # printing when successful
        if route != None:
            return route[0]
        else:
            return float('-inf')

    #################################################################################################################
    # Input:    node ids of two points: from_node_id and to_node_id
    # Output:   routing distance between two points
    # function: based on spatialite routing return the shortest path distance between "from_node_id" to "to_node_id"
    #################################################################################################################

    def route_distance_node_id(self, from_node_id, to_node_id):
        if from_node_id != None and to_node_id != None:
            distance_query = "SELECT  ST_Length(geometry) AS lenght FROM roads_net WHERE NodeFrom=%s AND NodeTo=%s;" % (
            from_node_id, to_node_id)
            self.cur.execute(distance_query)
            route = self.cur.fetchone()
            # printing when successful
        if route != None:
            return route[0]
        else:
            return float('-inf')