# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 14:08:48 2017

@author: apola
"""

import csv
import time
from datetime import datetime
import os
from uuid import getnode as get_mac

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
        
def time2int(s):
    return int(s[:2])*60+int(s[3:5])

def time2intS(s):
    return int(s[:2])*3600+int(s[3:5])*60+int(s[6:8])  
    

#%%     
def Get_required_V():
    ## Read file name of days --> from Jan 1-->Dec 31
    m_file_list_dir = os.path.abspath('processed/file_list.csv')
    m_file_list_name = list()
    with open(m_file_list_dir,'rb') as csvfile:
        rowspam=csv.reader(csvfile, delimiter=',')
        for i in rowspam:
            m_file_list_name.append(i[0])
    
    ## Create a processed list, we can syc this file to make multiple machine work together. 
    m_processed_list_dir = os.path.abspath('processed/Profit_Morning_Driver_processed_list.csv')
    if(not os.path.isfile(m_processed_list_dir)):
        with open(m_processed_list_dir,'a') as csvfile:
            rowWspam=csv.writer(csvfile,delimiter=',')
            rowWspam.writerow(['File created',get_mac(),time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())])
            
    m_cnt_processed=0
    with open(m_processed_list_dir,'a+') as csvfile:
        rowspam=csv.reader(csvfile, delimiter=',')
        for i in rowspam:
            m_cnt_processed+=1
        m_ready_to_processed=m_file_list_name[m_cnt_processed-1]
        rowWspam=csv.writer(csvfile,delimiter=',')
        rowWspam.writerow([m_ready_to_processed, get_mac(),time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())])
    
    # check deluse dir is existed or not, if not, create dir     
    m_subsample_dir=os.path.abspath('YearSim/'+m_ready_to_processed[0:8])    
    m_is_dir_exist = os.path.isdir(m_subsample_dir)
    if(not m_is_dir_exist):
        os.makedirs(m_subsample_dir)
       
    print 'File is generated at: '+time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    
    return m_ready_to_processed,m_subsample_dir,m_cnt_processed        
  
time_format = '%Y-%m-%d %H:%M:%S'


#%%
m_cnt_processed=0
while(m_cnt_processed<365):
    
    m_ready_to_processed,m_subsample_dir,m_cnt_processed = Get_required_V()
    
    taxi_id_dict={}
    taxi_id_dict_revenue={}
    taxi_id_car = {}
    c = 0
    pr_time = 0
    trip_dis = []
    taxi_start = {}
    taxi_end = {}
    taxi_driver_except = []

    
    m_file = '../data/NY_Sorted_New/'+m_ready_to_processed
    time2start = '04:00:00'    
    time2break = '17:00:00'
    with open(m_file,'rb') as csvfile:
        spamrow = csv.reader(csvfile,delimiter=',')
        for row in spamrow:
            if(c%10000==0):
                print 'Processing '+row[5][0:20]+"  ----->count is : " + str(c)+ "  ------>time taken :" + str(time.time()-pr_time)[0:4]            
                pr_time=time.time()
            c = c + 1
            # check if the date format is cprrect
            try:
                trip_start_time = datetime.strptime(row[5][0:20],time_format)
            except ValueError:
                continue
            
            if(time2int(time2start)>time2int(row[5][11:20])):
                continue
            elif(time2int(row[5][11:20])>time2int(time2break)):
                break
            
            if(not (is_number(row[8])) or int(row[8])==0):
                continue
            else:
                travel_time = int(row[8])
                if(travel_time>=3600):
                    continue
            
            if(float(row[9])*1.60934>=50):
                continue
            
            if(float(row[14])>70 or float(row[15])>10):
                continue

           
            tID = row[1]        
            dis_rec = float(row[9])*1609.34
            trip_dis.append(dis_rec/travel_time*3600.)

            if(tID in taxi_id_dict):
                taxi_id_dict[tID].append(dis_rec)
                taxi_id_dict_revenue[tID].append(float(row[14])+float(row[15])-dis_rec/1609.34/30.*2.5)
            else:
                taxi_id_dict.update({tID:[]})
                taxi_id_dict[tID].append(dis_rec)  
                
                taxi_id_dict_revenue.update({tID:[]})
                taxi_id_dict_revenue[tID].append(float(row[14])+float(row[15])-dis_rec/1609.34/30.*2.5)
                        

            if(tID in taxi_start):
                if(taxi_id_car[tID] != row[0]):
                    taxi_driver_except.append(tID)
                
                if(time2intS(row[5][11:20])<taxi_end[tID]):
                    if(not tID in taxi_driver_except):
                        taxi_driver_except.append(tID)
                    
                if(time2intS(row[6][11:20])>taxi_end[tID]):
                    taxi_end[tID] = time2intS(row[6][11:20])

            else:
                taxi_start.update({tID:time2intS(row[5][11:20])})
                taxi_end.update({tID:time2intS(row[6][11:20])})
                taxi_id_car.update({tID:row[0]})
                
                
    taxi_id_dr_dis = {} 
    taxi_id_revenue = {}
    

    for i in taxi_driver_except:
        if(i in taxi_id_dict):
            del taxi_id_dict[i]
            del taxi_id_dict_revenue[i]
            del taxi_end[i]
            del taxi_start[i]
        
    taxi_id_dr_dis = {} 
    taxi_id_revenue = {}  
    taxi_work_hr = {}    
    for index,i in enumerate(taxi_id_dict):
        ### check this condition, it is constraint for driver to work from 0400--1730
        ### You can possiblilly remove this condition
        if(taxi_start[i]<12*3600 and taxi_end[i]>5*3600+1800): 
            taxi_id_dr_dis.update({i:sum(taxi_id_dict[i])})
            taxi_id_revenue.update({i:sum(taxi_id_dict_revenue[i])})
            taxi_work_hr.update({i:((taxi_end[i]-taxi_start[i])/3600.)})
    ### write result to csv file
    with open(m_subsample_dir+'/taxi_driver_based.csv', 'w') as fp:
        z = csv.writer(fp, delimiter=',')
        z.writerow(['ID','profit','work hour','distance'])
        for e in taxi_id_revenue:
            z.writerow([e,"{:.2f}".format(taxi_id_revenue[e]),"{:.2f}".format(taxi_work_hr[e]),"{:.2f}".format(taxi_id_dr_dis[e])])
    


    

    
    
    
    
    
    
    
