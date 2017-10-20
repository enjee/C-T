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
        """
        Get the N nearest restaurants for a specific location
        :param lat:         The latitude of the center location
        :param lon:         The longitude of the center location
        :param price:       The price to filter the restaurants with
        :param categories:  The food categories to filter restaurants with
        :param limit:       The number of restaurants to return
        :return:            Give the closest N restaurants as return dictionary
        """

        # Iterate over all restaurants and check if they can be added to the filtered_restaurants list
        filtered_restaurants = []
        for id in range(len(self.df_restaurants)):
            if price != str(self.df_restaurants['price'][id]):
                continue
            if not categories or categories.lower() in str(self.df_restaurants['categories'][id]).lower():
                current_distance = self.calculate_distance((lat, lon), self.get_lat_lon(id))
                filtered_restaurants.append((id, current_distance))
        if len(filtered_restaurants) == 0:
            return {"nearest_restaurants": {"error": "None found"}}

        # Now order the filtered restaurants by distance and return the closest N
        nearest_restaurants = sorted(filtered_restaurants, key=lambda tup: tup[1])
        for i in range(len(nearest_restaurants)):
            nearest_restaurants[i] = self.format_restaurant(nearest_restaurants[i][0])
        return {"nearest_restaurants": nearest_restaurants[0: int(limit)]}

    def get_lat_lon(self, row_nr):
        """
        Get the latitude and longitude from a specific row inside the restaurants dataframe
        """
        data = ast.literal_eval(self.df_restaurants['coordinates'][row_nr])
        j = json.dumps(data)
        dict = json.loads(j)
        latitude = dict['latitude']
        longitude = dict['longitude']
        return (float(latitude), float(longitude))

    def calculate_distance(self, current, compare):
        """
        Calculate the distance between two points on the globe in km
        """
        lon1, lat1, lon2, lat2 = map(radians, [current[1], current[0], compare[1], compare[0]])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return km

    def get_all_restaurants(self):
        """
        Get all restaurants from the dataset
        """
        restaurants = []
        for i in range(len(self.df_restaurants)):
            restaurants.append(self.format_restaurant(i))
        return restaurants

    def format_restaurant(self, index):
        """

        :param index:
        :return:
        """
        restaurant = self.df_restaurants[index: index + 1]
        latlon = self.get_lat_lon(index)

        return {
            'latitude': latlon[0],
            'longitude': latlon[1],
            'title': restaurant['id'].item(),
            'price': restaurant['price'].item(),
            'categories': restaurant['categories'].item().decode('utf-8', 'ignore'),
            'id': index
        }
