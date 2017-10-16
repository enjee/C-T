import pandas as pd
import json
import ast
from math import radians, cos, sin, asin, sqrt

class Filter():
    def __init__(self, io, data_handler):
        self.data_handler = data_handler
        self.io = io

    def get_nearest_restaurant(self, lat, lon):
        self.df_restaurants = self.io.data_file
        nearest_distance = (-1, 100000000)
        print "Looping all restaurants"
        for i in range(len(self.df_restaurants)):
            current_distance = self.calculate_distance((lat, lon), self.get_lat_lon(i))
            if current_distance < nearest_distance[1]:
                nearest_distance = (i, current_distance)
                print nearest_distance
        return {"nearest_restaurant": self.df_restaurants[nearest_distance[0] : nearest_distance[0] + 1].to_json() }

    def get_lat_lon(self, row_nr):
        data = ast.literal_eval(self.df_restaurants['coordinates'][row_nr])
        j = json.dumps(data)
        dict = json.loads(j)
        latitude = dict['latitude']
        longitude = dict['longitude']
        return (float(latitude), float(longitude))

    def calculate_distance(self, current, compare):
        lon1, lat1, lon2, lat2 = map(radians, [current[1], current[0], compare[1], compare[0]])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return km