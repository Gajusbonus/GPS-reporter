#!/usr/bin/python
# sudo apt-get install python-pip build-essential python-dev python-wheel
# sudo pip install geopy gpxpy
import gpxpy, sys
from geopy.geocoders import Nominatim
from math import atan2, cos, sin, sqrt, radians
import re
import time, datetime
from datetime import date, timedelta

if len(sys.argv)== 0 :
    print "this script takes a filename as argument"
    sys.exit(2)
else:
    f1 = sys.argv[1]
    print "verwerken bestand: ", str(f1)
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

def zoekadres(point):
    geolocator = Nominatim()
    place1 = (point.latitude , point.longitude)
    location = geolocator.reverse(place1)
    s = (location.address).encode('iso8859-15')
    postcode = re.findall(r"\d{4}\s*[A-Z]{2}", s)
    if postcode == None:
        postcode = "Onbekende locatie"
    else:
        return postcode[0]

#show_times
# todo: print header
for track in gpx.tracks:
    for segment in track.segments:
        for p, point in enumerate(segment.points):
            if point.time != None:
                if p == 0:
                    t1 = point.time
                    t2 = point.time
                    rittijd = datetime.timedelta(seconds=0)   #reset time
                    postcode = zoekadres(point)
                    last_point = point
                    print p, t1.strftime('We starten op %H:%M:%S'), 'rittijd = ', rittijd, 'vertrek van: ', postcode
                if p == 1:
                    tijdsverschil = point.time - last_point.time
                    print "het tijdsverschil is:",  tijdsverschil
                    rittijd = rittijd + tijdsverschil
                    print '{0} t1 = {1} tijdsverschil = {2} totaal = ' .format(p, tijdsverschil, rittijd)
                    #t1 = t2 # zet het klaar om opnieuw een verschil te meten
                    if tijdsverschil > datetime.timedelta(seconds=300): #er is 5 minuten niet gereden
                        rittijd = datetime.timedelta(seconds=0)   #zet de tijd op nul
                        postcode = zoekadres(point)
                        print p, t1.strftime('We starten op %H:%M:%S'), 'tracktijd = ', rittijd, 'vertrek van: ', postcode
                    last_point = point
                if p > 1:
                    tijdsverschil = point.time - last_point.time
                    print "het tijdsverschil is:",  tijdsverschil
                    if tijdsverschil > datetime.timedelta(seconds=300): #er is 5 minuten niet gereden
                        tracktijd = datetime.timedelta(seconds=0)   #zet de tijd op nul
                        postcode = zoekadres(last_point)
                        print p, t1.strftime('We starten op %H:%M:%S'), 'tracktijd = ', tracktijd, 'vertrek van: ', postcode
                    
                    rittijd = rittijd + tijdsverschil
                    print p, last_point.time.strftime('last_point is %H:%M:%S'), point.time.strftime('dit punt is %H:%M:%S'), #'tracktijd = {0}'.format( tracktijd)
                    last_point = point
                    t1 = t2 # zet het klaar om opnieuw een verschil te meten

"""
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
"""
#t1 = datetime.strptime(str(point.time), "%Y-%m-%d %H:%M:%S")
# There are more utility methods and functions...
# You can manipulate/add/remove tracks, segments, points, waypoints and routes and
# get the GPX XML file from the resulting object:

#print 'GPX:', gpx.to_xml()
