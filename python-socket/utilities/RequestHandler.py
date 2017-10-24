import json
from FileIO import FileIO
from Filter import Filter


class RequestHandler():
    #######################################################
    # Constructor, save the socket (data handler) that created this request handler
    #######################################################
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.io = FileIO(data_handler)
        self.filter = Filter(self.io, self.data_handler)

    #######################################################
    # Receive a message from the web application through the socket
    # Handle the request by referring the data to a helper method
    #
    # This could be considered the server-socket side API
    #######################################################
    def receive(self, message):
        try:
            request = json.loads(message)
            if 'type' not in request:
                self.data_handler.send({'error': 'invalid call'})

            if request['type'] == 'ping':
                self.ping_request(request)

            if request['type'] == 'nearest':
                self.nearest_request(request)

            if request['type'] == 'all_restaurants':
                self.all_restaurants_request(request)

            if request['type'] == 'update':
                self.update_dataset_request(request)

            if request['type'] == 'equal':
                self.equal_request(request)


        except ValueError:
            print "Error, {} is not a json object".format(message)
            self.data_handler.send({'error': "{} is not a json object".format(message)})
        except KeyError as e:
            self.data_handler.send({'error': "Missing parameter {0} in: {1}".format(e.args[0], message)})

    #######################################################
    # Helper methods for handling specific requests       #
    #######################################################

    def ping_request(self, request):
        self.data_handler.send({'ping': 'pong'})

    def nearest_request(self, request):
        lat = float(request['latitude'])
        lon = float(request['longitude'])
        price = request['price']
        limit = request['limit']
        categories = None
        if 'categories' in request:
            categories = request['categories']
        self.data_handler.send(self.filter.get_nearest_restaurant(lat, lon, price, categories, limit))

    def all_restaurants_request(self, request):
        self.data_handler.send({'all_restaurants': self.filter.get_all_restaurants()})

    def update_dataset_request(self, request):
        self.data_handler.send({'updating': True})
        self.io.update_dataset()

    def equal_request(self, request):
        current_restaurant = request['restaurant']
        limit = request['limit']
        self.data_handler.send(self.filter.get_equal_restaurants(current_restaurant, limit))
