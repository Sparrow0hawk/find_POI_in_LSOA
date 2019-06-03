import requests
import json
import pandas as pd
from shapely.geometry import shape, Point
from geopy.geocoders import Nominatim
from collections import Counter
import sys

def get_POI_in_LSOA(location=None, POI_type=None):

    # first get the location from the text argument passed
    geolocator = Nominatim(user_agent='My_app')

    location = geolocator.geocode(str(location))

    loc_name = location.raw['display_name'].split(',')[0]

    # overpass API call

    overpass_url = 'http://overpass-api.de/api/interpreter'

    overpass_query = '''
    [out:json];
    (area[name='''+loc_name+''']; )->.searchArea;
    (node["amenity"='''+POI_type+'''](area.searchArea);
     way["amenity"='''+POI_type+'''](area.searchArea);
     rel["amenity"='''+POI_type+'''](area.searchArea);
    );
    out center;
    '''

    response = requests.get(overpass_url,
                       params={'data':overpass_query})

    # get API data in json format
    data = response.json()

    # open geojson data with lsoa polygons for west yorkshire
    geojson_data = requests.get('https://raw.githubusercontent.com/Sparrow0hawk/policedata_dump/master/WY_geojson.geojson').json()

    # loop through point lon/lat data to check which LSOA polygon the point is in
    poi_count = []

    for x in range(len(data['elements'])):
        try:
            point = Point(data['elements'][x]['lon'],data['elements'][x]['lat'])
        except KeyError:
            point = Point(data['elements'][x]['center']['lon'],data['elements'][x]['center']['lat'])

        for feature in geojson_data['features']:

            polygon = shape(feature['geometry'])

            if polygon.contains(point):
                poi_count.append(str(feature['properties']['LSOA11CD']))

    # return this as a pandas series
    return pd.Series(Counter(poi_count))

result = get_POI_in_LSOA(location=str(sys.argv[1]), POI_type=sys.argv[2])

print(result)
