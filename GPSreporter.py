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

if len(sys.argv)== 0 :
    print( "this script takes a filename as argument")
    sys.exit(2)
else:
    f1 = sys.argv[1]
    print( "importing file: ", str(f1))
    f = open(f1, 'r')

def calc_distance(origin, destination):
    """great-circle distance between two points on a sphere from their longitudes and latitudes"""
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km. earth

    dlat = radians(lat2-lat1)
    dlon = radians(lon2-lon1)
    a = (sin(dlat/2) * sin(dlat/2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2) * sin(dlon/2))
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = radius * c

    return d

gpx = gpxpy.parse(f)

def searchzip(point):
    geolocator = Nominatim()
    place1 = (point.latitude , point.longitude)
    location = geolocator.reverse(place1)
    s = (location.address).encode('iso8859-15')
    zipcode = re.findall(r"\d{4}\s*[A-Z]{2}", str(s))
    if zipcode == None:
        zipcode = "unknown location"
    else:
        return zipcode[0]

def searchaddress(point):
    geolocator = Nominatim()
    place1 = (point.latitude , point.longitude)
    location = geolocator.reverse(place1)
    s = (location.address).encode('iso8859-15')
    return str(s)

#show_times
# todo: print header
trackno = 0
for track in gpx.tracks:
    trackno = trackno + 1
    print( "track number: ", str(trackno))
    for segment in track.segments:			#
        for p, point in enumerate(segment.points):
            if point.time != None:
                if p == 0:
                    t1 = point.time
                    t2 = point.time
                    traveltime = datetime.timedelta(seconds=0)   #zet de tijd op nul
                    zipcode = searchzip(point)
                    address=searchaddress(point)
                    last_point = point
                    print( p, t1.strftime('Starting at %H:%M:%S'), 'address = ', address, 'depart from: ', zipcode)
                if p == 1:
                    deltatime = point.time - last_point.time
                    print( "time-difference:",  deltatime)
                    traveltime = traveltime + deltatime
                    print( '{0} t1 = {1} deltatime = {2}' .format(p, deltatime, traveltime))
                    #t1 = t2 # prepare for new reading of time difference
                    if deltatime > datetime.timedelta(seconds=300): # 5 minutes no driving?
# improve on: speed = 0.0 twice?
                        traveltime = datetime.timedelta(seconds=0)   # reset timer
                        zipcode = searchzip(point)
                        print( p, t1.strftime('Starting at %H:%M:%S'), 'traveltime = ', traveltime, 'depart from: ', address, zipcode)
                    last_point = point
                if p > 1:
                    deltatime = point.time - last_point.time
                    #print( "deltatime:",  deltatime)
                    if deltatime > datetime.timedelta(seconds=300): # 5 minutes no driving?
                        traveltime = datetime.timedelta(seconds=0)   # reset timer
                        zipcode = searchzip(last_point)
                        print( p, t1.strftime('Starting at %H:%M:%S'), 'traveltime = ', traveltime, 'depart from: ', zipcode)
                    traveltime = traveltime + deltatime
                    print(p, last_point.time.strftime('last_point is %H:%M:%S'), point.time.strftime('current point %H:%M:%S'), 'traveltime = {0}'.format( traveltime))
                    last_point = point
                    t1 = t2 # prepare for new reading of time difference

