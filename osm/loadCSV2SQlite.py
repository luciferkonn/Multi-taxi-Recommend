import csv, sqlite3, os
import pandas as pd
from pandas.io import sql
import subprocess

# for num in range(1, 366):
#     try:
#         f = open("./data/sorted/0_" + str(num) + ".csv")
#     except IOError as e:
#         continue
#     f.close()
#     in_csv = "./data/sorted/0_"+str(num)+".csv"
#     out_sqlite = './data/sorted_by_day/nyData_Monday_'+str(num)+'.sqlite'
#     table_name = 'my_table'
#     chunksize = 100000
#
#     columns = ['taxi_id', 'driver_id', 'un1', 'un2', 'un5', 'pickup_time', 'drop_time', 'un3', 'travel_time', \
#                'dist', 'pickup_lon', 'pickup_lat', 'drop_lon', 'drop_lat', 'base_fare', 'tax1', 'tax2', 'tax3', \
#                'tax4', 'final_fare']
#
#     nlines = subprocess.check_output(['wc', '-l', in_csv])
#     nlines = int(nlines.split()[0])
#
#     cnx = sqlite3.connect(out_sqlite)
#
#     for i in range(1, nlines, chunksize):
#         df = pd.read_csv(in_csv,
#                          header=None,
#                          nrows=chunksize,
#                          skiprows=i)
#
#         df.columns = columns
#
#         sql.to_sql(df,
#                    name=table_name,
#                    con=cnx,
#                    index=False,
#                    index_label='molecule_id',
#                    if_exists='append')
#     cnx.close()
in_csv = '../../data/sorted_by_week/sorted/Sunday.csv'
out_sqlite = '../../data/sorted_by_week/nyData_Sunday.sqlite'

table_name = 'my_table'
chunksize = 100000


columns = ['taxi_id', 'driver_id', 'un1', 'un2', 'un5', 'pickup_time', 'drop_time', 'un3', 'travel_time',\
           'dist', 'pickup_lon', 'pickup_lat', 'drop_lon', 'drop_lat', 'base_fare', 'tax1', 'tax2', 'tax3',\
           'tax4', 'final_fare']


nlines = subprocess.check_output(['wc', '-l', in_csv])
nlines = int(nlines.split()[0])


cnx = sqlite3.connect(out_sqlite)


for i in range(1, nlines, chunksize):

    df = pd.read_csv(in_csv,
                     header=None,
                     nrows=chunksize,
                     skiprows=i)

    df.columns = columns

    sql.to_sql(df,
               name=table_name,
               con=cnx,
               index=False,
               index_label='molecule_id',
               if_exists='append')
cnx.close()
# path = '/home/lucifer/Documents/CPSLAB/EV/solar_routing/data/NY_Sorted_New'
# files = os.listdir(path)
# s= []
#
# for file in files:
#     s.append(file)

# conn = sqlite3.connect('./data/sorted_by_week/nyData_Monday.db')
# cur = conn.cursor()
# cur.execute("""create table if not exists ny_sorted (taxi_id TEXT , \
# driver_id varchar(50), un1 varchar(10), un2 int(1), un5 varchar(10), pickup_time TEXT, drop_time TEXT, un3 int(1), travel_time int(1000000), dist float(10,6), pickup_lon float(20,10),\
# pickup_lat float(20,10),\
# drop_lon float(20,10),drop_lat float(20,10), base_fare REAL, \
# tax1 REAL, tax2 float(10,3), tax3 float(10,3), tax4 float(10,3), final_fare REAL)""")
# conn.commit()
#
# #for t in s:
#     #with open(t, 'rb') as fin:
# with open('./data/sorted_by_week/Monday.csv','rb') as fin:
#         dr = csv.DictReader(fin)
#         to_db = [(i['taxi_id'], i['driver_id'], i['un1'], i['un2'], i['un5'],i['pickup_time'
#          ], i['drop_time'], i['un3'], i['travel_time'], i['dist'], i['pickup_lon']
#          , i['pickup_lat'], i['drop_lon'], i['drop_lat'], i['base_fare'],i['tax1'],i['tax2'],i['tax3'],i['tax4'],i['final_fare']) for i in dr]
# cur.executemany("""insert into ny_sorted (taxi_id, driver_id, un1, un2, un5, pickup_time, drop_time, un3, travel_time, dist, pickup_lon, pickup_lat, drop_lon, drop_lat,base_fare, tax1, tax2, tax3, tax4, final_fare) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);""", to_db)
# conn.commit()
#
# conn.close()
