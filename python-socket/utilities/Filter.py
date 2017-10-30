import json
import ast
from math import radians, cos, sin, asin, sqrt
import numpy


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
        for i in range(int(limit)):
            nearest_restaurants[i] = self.format_restaurant(nearest_restaurants[i][0])
        return {"nearest_restaurants": nearest_restaurants[0: int(limit)]}

    def get_all_restaurants(self):
        """
        Get all restaurants from the dataset
        """
        restaurants = []
        for i in range(len(self.df_restaurants)):
            restaurants.append(self.format_restaurant(i))
        return restaurants

    def get_equal_restaurants(self, current_restaurant, limit):
        """
        Get equal restaurants to the given restaurant
        """
        similarity_list = []
        for i in range(len(self.df_restaurants)):
            curr_similarity = numpy.corrcoef(self.get_profile(current_restaurant), self.get_profile(i))[0, 1]
            similarity_list.append((i, curr_similarity))
        equal_restaurants = sorted(similarity_list, key=lambda tup: tup[1], reverse=True)
        for i in range(int(limit)):
            equal_restaurants[i + 1] = self.format_restaurant(equal_restaurants[i + 1][0])
        return {"equal_restaurants": equal_restaurants[1: int(limit) + 1]}

    def get_categories(self):
        categories = []
        for i in range(len(self.df_restaurants)):
            categories += self.get_categories_from_string(self.df_restaurants['categories'][i])

        return list(set(categories))

    def get_yelpreviews(self, yelp_id):
        reviews = []
        for i in range(len(self.df_restaurants)):
            categories += self.get_categories_from_string(self.df_restaurants['categories'][i])

        return list(set(categories))

    ###################
    # Helper methods #
    ###################

    def get_profile(self, index):
        """
        Get an array with all 'profile' values about a restaurant.
        This array will always be filled with numbers (floats / ints)
        """
        restaurant_profile = []
        restaurant = self.df_restaurants[index: index + 1]
        latlon = self.get_lat_lon(index)

        restaurant_profile.append(latlon[0])  # latitude
        restaurant_profile.append(latlon[1])  # longitude
        try:
            restaurant_profile.append(len(restaurant['price'].item()))  # nr of $ signs
        except:
            restaurant_profile.append(0)  # nr of $ signs
        restaurant_profile.append(len(restaurant['categories'].item()))  # nr of categories
        restaurant_profile.append(restaurant['rating'].item())  # rating (0.5 - 5.0)
        restaurant_profile.append(int(restaurant['review_count'].item()))  # nr of reviews
        return restaurant_profile

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

    def format_restaurant(self, index):
        """
        Format a restaurant by index (ID)
        """
        restaurant = self.df_restaurants[index: index + 1]
        latlon = self.get_lat_lon(index)

        return {
            'latitude': latlon[0],
            'longitude': latlon[1],
            'title': restaurant['id'].item(),
            'price': restaurant['price'].item(),
            'rating': restaurant['rating'].item(),
            'review_count': int(restaurant['review_count'].item()),
            'categories': restaurant['categories'].item().decode('utf-8', 'ignore'),
            'id': index,
            'yelp_id': restaurant['id'].item(),
            'location': restaurant['location'].item()
        }

    def get_categories_from_string(self, string):
        categories = []
        list =  string.encode("ascii").replace("'", "").split(" ")
        list = [word[1:] for word in list]
        list = list[1:]

        for i in range(len(list)):
            if list[i] == "title:":
                categories.append(list[i+1].split("}")[0])
        return categories
