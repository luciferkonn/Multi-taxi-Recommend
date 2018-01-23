import csv
from datetime import datetime
num = 0


for mon in range(1, 13):
    for day in range(1, 32):
        if mon in {'04', '06', '09', 11} and day == 31:
            continue
        if mon == '02' and day in {29, 30, 31}:
            # print("in***")
            continue
        if mon in {1, 2, 3, 4, 5 ,6 ,7 ,8 ,9}:
            mon = "0" + str(mon)
        if day in {1, 2, 3, 4, 5 ,6 ,7 ,8 ,9}:
            day = "0" + str(day)
        num += 1
        week = datetime.strptime("2013"+str(mon)+str(day), "%Y%m%d").weekday()
        toName = './data/sorted/' + str(week) + '_' + str(num) + '.csv'
        fromName = './data/13_' + str(mon) + '_' + str(day) + '_sorted.csv'
        print(str(week) + '* ' + str(mon) + '* ' + str(day))
