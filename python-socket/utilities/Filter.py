import pandas as pd
import json
import ast
from math import radians, cos, sin, asin, sqrt

class Filter():
    def __init__(self, io, data_handler):
        self.data_handler = data_handler
        self.io = io
        self.df_restaurants = self.io.data_file

    def get_nearest_restaurant(self, lat, lon, price, categories, limit):
        nearest_distance = []
        for i in range(len(self.df_restaurants)):
            current_distance = self.calculate_distance((lat, lon), self.get_lat_lon(i))

            if categories:
                current_categories = str(self.df_restaurants['categories'][i])
                if categories.lower() in current_categories.lower():
                    current_price = str(self.df_restaurants['price'][i])
                    if (current_price == price):
                        nearest_distance.append((i, current_distance))
            else:
                current_price = str(self.df_restaurants['price'][i])
                if (current_price == price):
                    nearest_distance.append((i, current_distance))

        if len(nearest_distance) == 0:
            return {"nearest_restaurants": "{ \"error\": \"None found\" }"}

        nearest_restaurants = sorted(nearest_distance, key=lambda tup: tup[1])
        for i in range(len(nearest_restaurants)):
            nearest_restaurants[i] = self.format_restaurant(nearest_restaurants[i][0])
        return {"nearest_restaurants": nearest_restaurants[0: limit] }

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

    def format_restaurant(self, index):
        restaurant = self.df_restaurants[index : index + 1]
        latlon = self.get_lat_lon(index)

        return {
            'latitude': latlon[0],
            'longitude': latlon[1],
            'title': restaurant['id'].item(),
            'price': restaurant['price'].item(),
            'categories': restaurant['categories'].item().decode('utf-8', 'ignore'),
            'id': index
        }