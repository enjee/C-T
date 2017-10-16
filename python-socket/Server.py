# INSTALL DEPENDENCIES: pip install tornado
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from utilities.DataHandler import DataHandler

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers = [(r"/", DataHandler)])
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8989)
    tornado.ioloop.IOLoop.instance().start()

