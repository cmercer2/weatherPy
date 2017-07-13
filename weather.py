"""
Get Weather info for a requested location, using Dark Sky API
"""

import requests
from geopy.geocoders import Nominatim
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.cfg')
API_KEY = config.get('APIsection', 'DSkey')
GEO = Nominatim()
USER_CITY = raw_input("Where do you want weather information from? ")

def convert_lat_long(city):
    """
    use geopy to convert requested city into latitude and longitude coordinates needed for api call
    """
    location = GEO.geocode(city)
    return (location.latitude, location.longitude)

LAT_LONG = convert_lat_long(USER_CITY)
print convert_lat_long(USER_CITY)

def get_api_response(latlong):
    """
    setup api url and return response text
    """
    loc = ",".join([str(i) for i in latlong])
    url = "https://api.forecast.io/forecast/{apikey}/{l}".format(apikey=API_KEY, l=loc)
    response = requests.request("GET", url)
    return response.text

print get_api_response(convert_lat_long(USER_CITY))