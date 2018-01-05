"""
Course timetable compiler 
We want to find the common time periods a group of people can meet
(i.e. mutual free time), given their course index numbers. The course
indexes contain information about their class timing.
"""

import re
import seaborn
import numpy
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def print_timetable(timetable,list_0000to2330):
    print ('Time Mon Tue Wed Thu Fri')
    for time,day in zip(list_0000to2330,timetable):
        print(time, end=' ')
        print(day)
    return 0

def prepare_database():
    """Extract data from text file (in HTML) and save into lists
        Each list represents an index number's lecture/tutorial slot
        
        An index number can have multiple entries (lecture and tutorial)
        
        Example of an entry: (index, type, group, day, time, venue, remarks)
        ['68104', 'LEC/STUDIO', '2', 'TUE', '1630-1930', 'NIE5-02-07', '']"""

    with open("ay1718s2.txt") as textfile:
        html_code = textfile.read()

    clean_html = BeautifulSoup(html_code,"html.parser")

    tables = clean_html.findAll('table')

    database = []

    count = 0
    for table in tables:
        count += 1

        if count%2!=0: # if it's odd, i.e. the course code/name, skip 
            continue 

        else:
            table_row = table.find_all('tr')
            for b in table_row:
                oneindexnumber = []
                cols = b.find_all('td')
                colcount = 0 
                for c in cols:
                    colcount += 1
                    # print(c.text)
                    if (c.text):
                        oneindexnumber.append(c.text)
                    elif (colcount == 1):
                        # add last index in database 
                        oneindexnumber.append(database[-1][0])
                    else:
                        oneindexnumber.append("")
                if oneindexnumber:
                    database.append(oneindexnumber)
    
    # print(count)

    return database

def day_to_index(day):
    if day == 'MON':
        return 0
    elif day == 'TUE':
        return 1
    elif day == 'WED':
        return 2
    elif day == 'THU':
        return 3
    elif day == 'FRI':
        return 4
    else:
        print("Error translating day (string) to index (int)")
        return -1

def add_to_master_timetable(user_input_index,course_database,timetable,list_0000to2330):
    for row in course_database:
        if row[0]==user_input_index:
            day = row[3]
            day_index = day_to_index(day)
            time_range = row[4]
            start_end_time = time_range.split('-')

            flag = False
            time_index = 0
            for timeslot in timetable:
                if list_0000to2330[time_index]==start_end_time[0]:
                    flag = True
                elif list_0000to2330[time_index]==start_end_time[1]:
                    flag = False
                else:
                    pass

                if flag:
                    ## between [starttime,endtime)
                    # print(day_index)
                    # print(time_index)
                    timetable[time_index][day_index] += 1
                time_index +=1
    return 0

def print_heatmap(timetable,list_0000to2330):
    numpy_timetable = numpy.array(timetable)
    seaborn.set()
    heatmap = seaborn.heatmap(numpy_timetable, yticklabels=1, linewidths=.25)
    # heatmap.gca().invert_yaxis()
    # heatmap.invert_yaxis()

    heatmap.set_title("Heatmap of timetable")
    heatmap.set_xlabel("Day")
    heatmap.set_ylabel("Time")
    heatmap.set_xticklabels(['Mon','Tue','Wed','Thu','Fri'], rotation = 'vertical')
    heatmap.set_yticklabels(list_0000to2330,fontsize=5)
    # reversed_time = list_0000to2330[::-1]
    # heatmap.set_yticklabels(reversed_time,fontsize=10)
    
    plt.show()

### Main code here ###

## Prepare timetable and database 
master_timetable = [[0]*5 for x in range(48)]
time_list = ['%s%s' % (str(h).zfill(2),m) for h in range(0,24) for m in ('00','30')]
generated_database = prepare_database()
# e.g. ['68104', 'LEC/STUDIO', '2', 'TUE', '1630-1930', 'NIE5-02-07', '']

## Prompt user for input of index numbers 
# user_index = input("Enter index numbers, separated by comma: ")
user_index = "10152,10208,10192,32464,00592,10182"
user_index_list = user_index.split(',')
print("List of indexes: " + user_index)

## Process user input 
for index in user_index_list:
    print("Processing index " + index)
    add_to_master_timetable(index,generated_database,master_timetable,time_list)

## Print out the timetable (in text and heatmap) + recommendations 

print_timetable(master_timetable,time_list)
print_heatmap(master_timetable,time_list)

