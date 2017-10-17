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

            if request['type'] == 'ping':
                self.ping_request(request)

            if request['type'] == 'nearest':
                self.nearest_request(request)

            if request['type'] == 'locations':
                self.locations_request(request);

            if request['type'] == 'update':
                self.update_dataset_request(request)


        except(ValueError):
            print "Error, {} is not a json object".format(message)
        # except:
        #     print "Bad request"
    #######################################################
    # Helper methods for handling specific requests
    #######################################################

    def ping_request(self, request):
        self.data_handler.send({'ping': 'pong'})

    def nearest_request(self, request):
        lat = float(request['latitude'])
        lon = float(request['longitude'])
        self.data_handler.send(self.filter.get_nearest_restaurant(lat, lon))

    def locations_request(self, request):
        self.data_handler.send( {'locations': self.filter.get_all_locations()} )

    def update_dataset_request(self, request):
        self.data_handler.send({'updating': True})
        self.io.update_dataset()
