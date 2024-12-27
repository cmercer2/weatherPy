# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Get Weather info for a requested location, using Dark Sky API
"""
import configparser
import json
import math
import datetime
import ssl
import certifi
import requests
from geopy.geocoders import Nominatim
from pick import pick
import emoji

ctx = ssl.create_default_context(cafile=certifi.where())

#read config file containing API key for darksky
CONFIG = configparser.ConfigParser()
CONFIG.read('CONFIG.ini')
API_KEY = CONFIG['APIsection']['PWkey']
GEO = Nominatim(user_agent="weatherPy", ssl_context=ctx)
DEG = "°"

#Ask user to input a location
USER_LOC = input("Where do you want weather information from? ")

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
    except Exception:
        print("Error processing your request. Trying again")
        continue
    else:
        break

def get_api_response(lat, lon):
    """ setup api url and return response """
    url = "https://api.pirateweather.net/forecast/{key}/{la},{lo}".format(key=API_KEY, la=lat, lo=lon)
    api_response = requests.request("GET", url)
    parsed = json.loads(api_response.text)
    #write response to file, just for development
    with open("weather.json", "w+") as openfile:
        json.dump(parsed, openfile, indent=4)
    return parsed

def get_date(timestamp):
    """ get date string from timestamp """
    date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%A %B %d, %Y')
    return date

def get_time(timestamp):
    """ get time string from timestamp"""
    time = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%I:%M %p')
    return time

#Get JSON
WTHR = get_api_response(LAT, LONG)
#Menu options for user to pick
USER_OPT = ["Current Conditions", "Weekly Forecast", "Hourly Conditions"]

def user_options(opt):
    """ ask user to pick one option for weather data """
    title = "What weather information do you want?"
    options = opt
    indicator = "->"
    choice = pick(options, title, indicator)
    return choice

USER_CHOICE = user_options(USER_OPT)

def get_weather_emoji(icon):
    """ get 'icon' from json, return emoji """
    if icon == "clear-day":
        weather_icon = emoji.emojize(':sun_with_face:', language='alias')
    elif icon == "clear-night":
        weather_icon = emoji.emojize(":crescent_moon:", language='alias')
    elif icon == "rain":
        weather_icon = emoji.emojize(":umbrella:", language='alias')
    elif icon == "snow":
        weather_icon = emoji.emojize(":snowflake:", language='alias')
    elif icon == "sleet":
        weather_icon = emoji.emojize(":sweat_drops:", language='alias')
    elif icon == "wind":
        weather_icon = emoji.emojize(":dash:", language='alias')
    elif icon == "fog":
        weather_icon = emoji.emojize(":foggy:", language='alias')
    elif icon == "cloudy":
        weather_icon = emoji.emojize(":cloud:", language='alias')
    elif icon == "partly-cloudy-day" or icon == "partly-cloudy-night":
        weather_icon = emoji.emojize(":partly_sunny:", language='alias')
    else:
        weather_icon = emoji.emojize(":earth_americas:", language='alias')
    return weather_icon

def get_cur_conditions():
    """ print current weather """
    cur_temp = int(math.ceil(WTHR["currently"]["temperature"]))
    cur_cond = WTHR["currently"]["summary"]
    precip_prob = WTHR["currently"]["precipProbability"]
    humidity = WTHR["currently"]["humidity"] * 100
    icon = get_weather_emoji(WTHR["currently"]["icon"])
    print("==========CURRENT CONDITIONS==========")
    print(get_full_location(USER_LOC))
    print(icon)
    print("Temperature: {temp}".format(temp=cur_temp))
    print("Conditions: {cond}".format(cond=cur_cond))
    print("Precipitation Chance: {pp}%".format(pp=precip_prob))
    print("humidity: {h}%".format(h=humidity))

def get_weekly_forecast():
    """print weekly forecast"""
    days = WTHR["daily"]["data"]
    print("==========WEEKLY FORECAST==========")
    print(WTHR["daily"]["summary"])
    for i in range(len(days)):
        summary = days[i]["summary"]
        min_temp = days[i]["temperatureMin"]
        max_temp = days[i]["temperatureMax"]
        forecast_string = "Forecast: {s}".format(s=summary)
        date = get_date(days[i]["time"])
        icon = get_weather_emoji(days[i]["icon"])
        print("-" * len(forecast_string))
        print(date)
        print(icon)
        print(forecast_string)
        print("High of {high}{d}, Low of {low}{d}".format(high=max_temp, low=min_temp, d=DEG))
        print("-" * len(forecast_string))

def get_hourly_forecast():
    """print hourly forecast"""
    hour = WTHR["hourly"]["data"]
    print("==========HOURLY FORECAST==========")
    print(WTHR["hourly"]["summary"])
    for i in range(len(hour)):
        temp = hour[i]["temperature"]
        summary = hour[i]["summary"]
        forecast = "Forecast: {s}".format(s=summary)
        icon = get_weather_emoji(hour[i]["icon"])
        if hour[i]["precipProbability"] == 0:
            precip_string = "No chance of precipitation"
        else:
            precip_prob = hour[i]["precipProbability"] * 100
            precip_type = hour[i]["precipType"]
            precip_string = "{c}% chance of {p}".format(c=precip_prob, p=precip_type)
        print("-" * len(forecast))
        print(get_time(hour[i]["time"]))
        print(icon)
        print("Temperature: {t}".format(t=temp))
        print(forecast)
        print(precip_string)
        print("-" * len(forecast))

if USER_CHOICE[1] == 0:
    get_cur_conditions()
elif USER_CHOICE[1] == 1:
    get_weekly_forecast()
else:
    get_hourly_forecast()
