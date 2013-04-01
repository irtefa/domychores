import os
import sys
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.options import options, define
from handlers.pages import IndexHandler
from handlers.pages import AboutHandler


PORT = sys.argv[1]

define("port", default=PORT, help="run on the given port", type=int)


class Application(tornado.web.Application):
    """ The primary API for DoMyChores"""

    def __init__(self):

        handlers = [
            tornado.web.URLSpec(r'/', IndexHandler),
            tornado.web.URLSpec(r'/about', AboutHandler)
        ]
        current_dir = os.path.dirname(__file__)

        settings = dict(
            template_path=os.path.join(current_dir, 'templates'),
            static_path=os.path.join(current_dir, 'static'),
            cookie_secret='947e5d1dc624bc99421bfc7e8ebad245'
        )

        super(Application, self).__init__(handlers, **settings)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
