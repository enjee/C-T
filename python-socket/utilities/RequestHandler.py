import json
from FileIO import FileIO
from FramePlayer import FramePlayer


class RequestHandler():
    #######################################################
    # Constructor, save the socket (data handler) that created this request handler
    #######################################################
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.io = FileIO(data_handler)
        self.player = FramePlayer(self.data_handler, self.io, 100)  # 100 is the number of ms between each frame

    #######################################################
    # Receive a message from the web application through the socket
    # Handle the request by referring the data to a helper method
    #
    # This could be considered the server-socket side API
    #######################################################
    def receive(self, message):
        try:
            request = json.loads(message)

            if request['type'] == 'play':
                self.play_request(request)

            elif request['type'] == 'time':
                self.time_request(request)

            elif request['type'] == 'load':
                self.load_request(request)

            elif request['type'] == 'showFiles':
                self.show_files_request(request)

            elif request['type'] == 'pause':
                self.pause_request(request)

            elif request['type'] == 'config':
                self.config_request(request)

            elif request['type'] == 'speed':
                self.speed_request(request)

            elif request['type'] == 'currentFrame':
                self.current_frame_request(request)

            elif request['type'] == 'focus':
                self.focus_request(request)

            else:
                print "Error, {} has no type specified or type is not recognizable".format(message)

        except(ValueError):
            print "Error, {} is not a json object".format(message)
    #######################################################
    # Helper methods for handling specific requests
    #######################################################

    def play_request(self, request):
        self.player.pause(False)

    def time_request(self, request):
        time = request['time']
        self.player.set_time(time)

    def load_request(self, request):
        file_name = request['file_name']
        self.io.load_file(file_name)
        self.player.current_time = 0
        self.player.counter = 0
        self.player.last_frame = None
        self.data_handler.send({"loading": "done"})

    def show_files_request(self, request):
        files = self.io.show_files()
        self.data_handler.send({"files": files})

    def pause_request(self, request):
        self.player.pause(request['pause'])
        self.data_handler.send({"isPaused": request['pause']})

    def config_request(self, request):
        self.data_handler.send(self.io.config)

    def speed_request(self, request):
        self.player.set_speed(request['speed'])
        self.data_handler.send({"speed" : self.io.config['match_settings']['speed']})

    def current_frame_request(self, request):
        current_frame = self.player.current_frame()
        self.data_handler.send({"current_frame" : current_frame})

    def focus_request(self, request):
        focus = request['focus']
        self.player.set_focus(focus)




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

            if request['type'] == 'location':
                self.location_request(request)

            else:
                print "Error, {} has no type specified or type is not recognizable".format(message)

        except(ValueError):
            print "Error, {} is not a json object".format(message)
    #######################################################
    # Helper methods for handling specific requests
    #######################################################

    def ping_request(self, request):
        self.data_handler.send({'ping': 'pong'})


    def location_request(self, request):
        location = request['location']
        # do stuff with location