"""
@author: Jikun Kang
"""
import math
from osm_grid import *
import numpy as np
import decimal
import time
import csv


def plot_distance():
    distance = np.loadtxt('./distance.txt', delimiter=' ', dtype=np.float32)
    print(distance)


if __name__ == '__main__':
    count = -1
    distance = np.zeros(365)
    time1 = np.zeros(365)
    ave_dist = np.zeros(365)
    ave_time = np.zeros(365)
    number = np.zeros(365)
    for i in range(1, 13):
        for j in range(1, 32):
            if i < 10:
                month = '0' + str(i)
            else:
                month = str(i)
            if j < 10:
                day = '0' + str(j)
            else:
                day = str(j)
            try:
                with open('../../data/original/13_'+month+'_'+day+'_sorted.csv', 'rb') as csvfile:
                    count += 1
                    spamreader = csv.reader(csvfile, delimiter=' ')
                    for row in spamreader:
                        words = row[2]
                        word = words.split(',')
                        time1[count] += float(word[2])
                        distance[count] += float(word[3])
                        number[count] += 1
                    ave_dist[count] = distance[count] / number[count]
                    ave_time[count] = time1[count] / number[count]
            except IOError as e:
                continue
    # print(distance)
    print(ave_dist)
    print(ave_time)
    np.savetxt('ave_dist', ave_dist)
    np.savetxt('ave_time', ave_time)
    # plot_distance()
    # b = np.zeros(10)


