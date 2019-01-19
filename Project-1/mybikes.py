# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 12:30:40 2018

@author: devin jones
@email:  daj59@pitt.edu
"""

import sys
import json
from requests import get
from math import cos, asin, sqrt


#Check to see if there is at least 3 arg before continuing
if(len(sys.argv) < 3):
    print("Missing argument(s) please check input and try again")
    exit()


URL = sys.argv[1]
if(URL[-1] == '/'):
    statusURL = (URL + 'station_status.json')
    infoURL = (URL + 'station_information.json')
    
else:
    statusURL = (URL + '/station_status.json')
    infoURL = (URL + '/station_information.json')
    


#get json files for status
try:
    file = get(statusURL)
    data = json.loads(file.content)
    dict_status_data = dict(data)['data']['stations']
except:
    print("\nExtension 'station_status.json' NOT AVAILABLE")

#get json files for info
try:
    file = get(infoURL)
    data = json.loads(file.content)
    dict_info_data = dict(data)['data']['stations']
except:
    print("\nExtension 'station_informations.json' NOT AVAILABLE")


#Store command into constant variable
COMMAND = sys.argv[2]



#create a dictionary from csv file to preform calculations
def getDict(reader):
    stations = []
    
    for station in reader:
        stations.append(dict(station))
    return(stations)
    
    
    
      
    
def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a)) 



   
#930 -- first total
#921


#####
# 1 #
################################################################
## TOTAL BIKES METHOD

if(COMMAND == 'total_bikes'):
    
    
    #Get number of bikes that are available and store them in list to sum up after
    bikes = [int(x['num_bikes_available']) for x in dict_status_data ] 
    
    Output = sum(bikes)
        
    print('\nCommand={}' .format(COMMAND))
    print('Parameters={}' .format(""))
    print('Output={}' .format(Output))






#####
# 2 # 
###############################################################################
## TOTAL DOCKS METHOD

if(COMMAND == 'total_docks'):

    
    #Get number of docks that are available and store them in list to sum up after
    bikes = [int(x['num_docks_available']) for x in dict_status_data ] 
    
    Output = sum(bikes)
        
    print('\nCommand={}' .format(COMMAND))
    print('Parameters={}' .format(""))
    print('Output={}' .format(Output))
 
    
    
    



#####
# 3 #    
###############################################################################
## PERCENTAGE AVAILABLE AT STATION METHOD

if(COMMAND == 'percent_avail'):
    #get json files
    
    try:
        stationID = sys.argv[3]
    except:
        print('ARGUMENT MISSING\n')
        exit()
        
    station = {}


    #Find the specified stations
    for stations in dict_status_data:
        if(stations['station_id'] == stationID):
            station = (dict(stations))
    if(station == {}):
        print('\nStation does not exist!')
        exit()

    numBikes = int(station['num_bikes_available'])
    numDocks = int(station['num_docks_available'])           
    
    Output = numDocks/(numBikes +numDocks) * 100
       
    
    print('\nCommand={}' .format(COMMAND))
    print('Parameters={}' .format(stationID))
    print('Output={:.0f}%' .format(Output))
    
        
    
 
    
    
    
    
    
    
#####
# 4 #    
###############################################################################
## NAME OF THE CLOSEST HealthyRidePGH METHOD 
    
if(COMMAND == 'closest_stations'):
    
    try:
        lat = sys.argv[3]
        lon = sys.argv[4]
    except:
        print('ARGUMENT MISSING\n')
        exit()
        
     #List to hold the 3 closest stations   
    closestStation  = []
    
    '''
    Go through each station and calculate the distance
    Add that station to the list of stations with is distance as a tuple(station, distance)
    Then sort that list by distance
    then create list of first 3 stations out of the sorted list and store them in a list
    continue till all stations were calculated
    '''
    for x in dict_info_data:
        dist = distance(float(lat), float(lon), float(x['lat']), float(x['lon']))
        
        #if(len(closestStation) <3):
        closestStation.append((x, dist))
        
        closestStation = sorted(closestStation, key = lambda t: t[1])[0:3]
    
    
    '''Format the Output'''
    Output1= (closestStation[0][0]['station_id'] + ', '
    + closestStation[0][0]['name'])
    
    Output2= (closestStation[1][0]['station_id'] + ', '
    + closestStation[1][0]['name'])
    
    Output3= (closestStation[2][0]['station_id'] + ', '
    + closestStation[2][0]['name'])

    print('\nCommand={}' .format(COMMAND))
    print('Parameters={} {}' .format(sys.argv[3], sys.argv[4]))
    print('Output=\n{}\n{}\n{}' .format(Output1, Output2, Output3))
    
#####
# 5 #    
###############################################################################
## CLOSEST STATION
## WITH AVAILABLE BIKES METHOD

if(COMMAND == 'closest_bike'):
    
    try:
        lat = sys.argv[3]
        lon = sys.argv[4]
    except:
        print('ARGUMENT MISSING\n')
        exit()
        
     #List to hold the 3 closest stations   
    closestStation  = []
    

    
    #Will hold the only the stations with available bikes
    dict_avail_bikes_data = []
    dict_stations_with_bikes = []
    
    for x in dict_status_data:
        if(x['num_bikes_available'] > 0):
            dict_avail_bikes_data.append(x)
        
    for x in dict_avail_bikes_data:
        for x1 in dict_info_data:
            if(x['station_id'] == x1['station_id']):
                dict_stations_with_bikes.append(x1)
    
        '''
    Go through each station and calculate the distance
    Add that station to the list of stations with is distance as a tuple(station, distance)
    Then sort that list by distance
    then create list of first 3 stations out of the sorted list and store them in a list
    continue till all stations were calculated
    '''
    
    for x in dict_stations_with_bikes:
        #print(x)
        dist = distance(float(lat), float(lon), float(x['lat']), float(x['lon']))
        
        
        #if(len(closestStation) <3):
        closestStation.append((x, dist))
        
        closestStation = [sorted(closestStation, key = lambda t: t[1])[0]]
    
    
    '''Format the Output'''
    Output1= (closestStation[0][0]['station_id'] + ', '
    + closestStation[0][0]['name'])

    print('\nCommand={}' .format(COMMAND))
    print('Parameters={} {}' .format(sys.argv[3], sys.argv[4]))
    print('Output={}' .format(Output1))
    
