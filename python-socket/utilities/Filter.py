import pandas as pd
import json
import ast
from math import radians, cos, sin, asin, sqrt

class Filter():
    def __init__(self, io, data_handler):
        self.data_handler = data_handler
        self.io = io
        self.df_restaurants = self.io.data_file

    def get_nearest_restaurant(self, lat, lon, price, categories):
        nearest_distance = (-1, 100000000)
        print "Looping all restaurants"
        for i in range(len(self.df_restaurants)):
            current_distance = self.calculate_distance((lat, lon), self.get_lat_lon(i))
            if current_distance < nearest_distance[1]:
                if categories:
                    current_categories = str(self.df_restaurants['categories'][i])
                    if categories.lower() in current_categories.lower():
                        current_price = str(self.df_restaurants['price'][i])
                        if (current_price == price):
                            nearest_distance = (i, current_distance)
                            print nearest_distance
                else:
                    current_price = str(self.df_restaurants['price'][i])
                    if (current_price == price):
                        nearest_distance = (i, current_distance)
                        print nearest_distance

        if nearest_distance[0] == -1:
            return {"nearest_restaurant": "{ \"error\": \"None found\" }"}
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

    def get_all_locations(self):
        # Loop over all restaurants and provide latitude, longitude and title
        locations = []
        for i in range(len(self.df_restaurants)):
            restaurant_location = {}
            latlon = self.get_lat_lon(i)
            restaurant_location['lat'] = latlon[0]
            restaurant_location['lon'] = latlon[1]
            restaurant_location['title'] = self.df_restaurants['id'][i]
            locations.append(restaurant_location)
        return locations
