import json
from FileIO import FileIO


class RequestHandler():
    #######################################################
    # Constructor, save the socket (data handler) that created this request handler
    #######################################################
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.io = FileIO(data_handler)

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

            else:
                print "Error, {} has no type specified or type is not recognizable".format(message)

        except(ValueError):
            print "Error, {} is not a json object".format(message)
    #######################################################
    # Helper methods for handling specific requests
    #######################################################

    def ping_request(self, request):
        self.data_handler.send({'ping': 'pong'})
