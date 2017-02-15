#!/usr/bin/env python3
# sudo apt-get install python-pip build-essential python-dev python-wheel
#sudo python3.4 -m pip install gpxpy geopy
#
import gpxpy, sys
from geopy.geocoders import Nominatim
from math import atan2, cos, sin, sqrt, radians
import re
import time, datetime
from datetime import date, timedelta

DEBUG = False # 'True' or 'False'

if (DEBUG == True):
    print( 'Debug ON')
#else:
#    print( 'Debug OFF')

if len(sys.argv)== 0 :
    print( "this script takes a filename as argument")
    sys.exit(2)
else:
    f1 = sys.argv[1]
    if (DEBUG == True):
        print( "importing file: ", str(f1))
    f = open(f1, 'r')
    gpx = gpxpy.parse(f)
    f.close()

def calc_distance(origin, destination):
    """great-circle distance between two points on a sphere from their longitudes and latitudes"""
    lat1, lon1 = last_point.latitude, last_point.longitude
    lat2, lon2 = point.latitude, point.longitude
    radius = 6371 # km. earth
    if (DEBUG == True):
        print(lat1, lon1, end='\n')
        print(lat2, lon2, end='\n')

    dlat = radians(lat2-lat1)
    dlon = radians(lon2-lon1)
    a = (sin(dlat/2) * sin(dlat/2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2) * sin(dlon/2))
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = radius * c

    return d

def searchaddress(point):
    geolocator = Nominatim()
    place1 = (point.latitude , point.longitude)
    location = geolocator.reverse(place1)
    s = (location.address)    #.encode('iso8859-15')
    return str(s)

def searchzip(point):
    s = searchaddress(point)
    zipcode = re.findall(r"\d{4}\s*[A-Z]{2}", str(s))
    if zipcode == None:
        zipcode = "unknown location"
    else:
        return zipcode[0]


#show_times
# todo: print header
trackno = 0
for track in gpx.tracks:
    trackno = trackno + 1
    for segment in track.segments:			#
        n = len(segment.points)
        if (DEBUG == True):
            print("track number: ", str(trackno), "number of points: ", n)
        for p, point in enumerate(segment.points):
            if point.time != None:
                if p == 0:
                    t1 = point.time
                    t2 = point.time
                    traveltime = datetime.timedelta(seconds=0)   #zet de tijd op nul
                    distance = 0
                    zipcode = searchzip(point)
                    address=searchaddress(point)
                    last_point = point
                    print(t1.strftime('Starting at %H:%M'))    #  %H:%M:%S
                    print(p,'-->Depart from: ', address, end='\n')
                if p == 1:
                    deltatime = point.time - last_point.time
                    if (DEBUG == True):
                        print( "time-difference:",  deltatime)
                    traveltime = traveltime + deltatime
                    distance = calc_distance(last_point, point)
                    if (DEBUG == True):
                        print( '{0} t1 = {1} deltatime = {2}' .format(p, deltatime, traveltime), end='\n' )
                        print("distance: ", distance)
                    #t1 = t2 # ready to meassure a time difference
                    if deltatime > datetime.timedelta(seconds=300): # 5 minutes no driving? improve on: speed = 0.0 twice?
                        traveltime = datetime.timedelta(seconds=0)   # reset timer
                        zipcode = searchzip(point)
                        print(p,"--> ", point.time.strftime('%H:%M Ended at: '), searchaddress(point), searchzip(point), end='\n')   
                        print("   Distance: {:.2f}" .format( distance), " km, ", 'Traveltime = {0}'.format( traveltime), end='\n\n') # check is this is reset

                    last_point = point
                if p > 1:
                    deltatime = point.time - last_point.time
                    #print( "deltatime:",  deltatime)
                    if deltatime > datetime.timedelta(seconds=300): # 5 minutes no driving?
                        traveltime = datetime.timedelta(seconds=0)   # reset timer
                        distance = distance + calc_distance(last_point, point)
                        zipcode = searchzip(last_point)
                        print(p,"Break at ", point.time.strftime('%H:%M '), searchaddress(point), searchzip(point), end='\n')
                        print("   Distance: {:.2f}" .format( distance), " km, ", 'Traveltime = {0}'.format( traveltime), end='\n\n') # check is this is reset
                    #elif (point.speed!=0.0 and last_point.speed==0.0):
                    #    print(p,point.speed, searchaddress(point))
                    traveltime = traveltime + deltatime
                    distance = distance + calc_distance(last_point, point)
                    if (DEBUG == True):
                        print(p, last_point.time.strftime('last_point is %H:%M:%S'), point.time.strftime('current point %H:%M:%S'), 'traveltime = {0}'.format( traveltime))
                    last_point = point
                    t1 = t2 # prepare for new reading of time difference
        #print(point.time.strftime('Ending at %H:%M'))
        print(p,"--> ", point.time.strftime('%H:%M Ended at: '), searchaddress(point), searchzip(point), end='\n')   
        print("   Distance: {:.2f}" .format( distance), " km, ", 'Traveltime = {0}'.format( traveltime), end='\n\n') # check is this is reset
