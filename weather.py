# -*- coding: utf-8 -*-
"""
Get Weather info for a requested location, using Dark Sky API
"""
import ConfigParser
import json
import math
import datetime

import requests
from geopy.geocoders import Nominatim
from pick import pick

CONFIG = ConfigParser.RawConfigParser()
CONFIG.read('CONFIG.cfg')
API_KEY = CONFIG.get('APIsection', 'DSkey')
GEO = Nominatim()
DEG = "°"
#Ask user to input a location
USER_LOC = raw_input("Where do you want weather information from? ")

def convert_lat_long(loc):
    """ use geopy to convert requested location into latitude and longitude needed for api call """
    location = GEO.geocode(loc, timeout=10)
    return (location.latitude, location.longitude)

def get_full_location(loc):
    """use geopy to get full location name"""
    full_loc = GEO.geocode(loc, timeout=10)
    return full_loc.address

while True:
    try:
        LAT, LONG = convert_lat_long(USER_LOC)
    except StandardError:
        print "Error processing your request. Trying again"
        continue
    else:
        break

def get_api_response(lat, lon):
    """ setup api url and return response """
    url = "https://api.forecast.io/forecast/{key}/{la},{lo}".format(key=API_KEY, la=lat, lo=lon)
    api_response = requests.request("GET", url)
    parsed = json.loads(api_response.text)
    #write response to file, just for development
    with open("weather.json", "w+") as openfile:
        json.dump(parsed, openfile, indent=4)
    return parsed

def get_date_time(timestamp):
    """ get date string from timestamp """
    date_time = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%A %B %d, %Y')
    return date_time

#Get JSON
WTHR = get_api_response(LAT, LONG)
#Menu options for user to pick
USER_OPT = ["Current Conditions", "Weekly Forecast", "Hourly Conditions"]

def user_options(opt):
    """ ask user to pick one option for weather data """
    title = "What weather information do you want?"
    options = opt
    indicator = "=>"
    choice = pick(options, title, indicator)
    return choice

USER_CHOICE = user_options(USER_OPT)

def get_cur_conditions():
    """ print current weather """
    cur_temp = int(math.ceil(WTHR["currently"]["temperature"]))
    cur_cond = WTHR["currently"]["summary"]
    precip_prob = WTHR["currently"]["precipProbability"]
    humidity = WTHR["currently"]["humidity"] * 100
    print "==========CURRENT CONDITIONS=========="
    print get_full_location(USER_LOC)
    print "Temperature: {temp}".format(temp=cur_temp)
    print "Conditions: {cond}".format(cond=cur_cond)
    print "Precipitation Chance: {pp}%".format(pp=precip_prob)
    print "humidity: {h}%".format(h=humidity)

def get_weekly_forecast():
    """print weekly forecast"""
    days = WTHR["daily"]["data"]

    print "==========WEEKLY FORECAST=========="
    print WTHR["daily"]["summary"]
    for i in range(len(days)):
        summary = days[i]["summary"]
        min_temp = days[i]["temperatureMin"]
        max_temp = days[i]["temperatureMax"]
        forecast_string = "Forecast: {s}".format(s=summary)
        time_stamp = days[i]["time"]
        date = get_date_time(time_stamp)
       
        print "-" * len(forecast_string)
        print date
        print forecast_string
        print "High of {high}{d}, Low of {low}{d}".format(high=max_temp, low=min_temp, d=DEG)
        print "-" * len(forecast_string)

if USER_CHOICE[1] == 0:
    get_cur_conditions()
elif USER_CHOICE[1] == 1:
    get_weekly_forecast()
else:
    print "HOURLY CONDITIONS"
