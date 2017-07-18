# -*- coding: utf-8 -*-
"""
Get Weather info for a requested location, using Dark Sky API
"""
import ConfigParser
import json
import Tkinter
import pprint
import math

import requests
from geopy.geocoders import Nominatim

config = ConfigParser.RawConfigParser()
config.read('config.cfg')
API_KEY = config.get('APIsection', 'DSkey')
GEO = Nominatim()
USER_CITY = raw_input("Where do you want weather information from? ")

def convert_lat_long(city):
    """ use geopy to convert requested city into latitude and longitude needed for api call """
    location = GEO.geocode(city)
    return (location.latitude, location.longitude)

LAT, LONG = convert_lat_long(USER_CITY)
#print convert_lat_long(USER_CITY)

def get_api_response():
    """ setup api url and return response """
    url = "https://api.forecast.io/forecast/{key}/{la},{lo}".format(key=API_KEY, la=LAT, lo=LONG)
    api_response = requests.request("GET", url)
    parsed = json.loads(api_response.text)
    return parsed
    
WTHR = get_api_response()

CUR_TEMP = int(math.ceil(WTHR["currently"]["temperature"]))

print "The Current Temperature in {city} is {temp}°".format(city=USER_CITY,temp=CUR_TEMP) 

