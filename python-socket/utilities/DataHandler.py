import tornado.websocket
import json
from RequestHandler import RequestHandler


#######################################################
# Basic Tornado socket implementation.
#
# Allows communication between the JavaScript
# web app and other python modules.
#######################################################
class DataHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print "Connection has been opened"
        self.request_handler = RequestHandler(self)
        self.send({"connection": "open"})
        print "Request handler has been created"

    def on_close(self):
        print "Connection has been closed"

    #######################################################
    # Message recieved, delegate to the request handler
    #######################################################
    def on_message(self, message):
        print "Message received: ", message
        self.request_handler.receive(message)

    #######################################################
    # Send a message, will always be serialized to JSON
    #######################################################
    def send(self, message):
        try:
            self.write_message(json.dumps(message))
            print "Message sent: ", message
        except Exception:
            self.close()

    #######################################################
    # Do not check for cross origin
    #######################################################
    def check_origin(self, origin):
        return True
