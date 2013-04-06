import os
import sys
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.options import options, define
from handlers.pages import IndexHandler
from handlers.pages import AboutHandler
from handlers.signup import SignupHandler
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *


PORT = sys.argv[1]

define("port", default=PORT, help="run on the given port", type=int)


class Application(tornado.web.Application):
    """ The main application class for DoMyChores"""

    def __init__(self):

        handlers = [
            tornado.web.URLSpec(r'/', IndexHandler),
            tornado.web.URLSpec(r'/about', AboutHandler),

            # API
            tornado.web.URLSpec(r'/api/signup', SignupHandler)
        ]
        current_dir = os.path.dirname(__file__)

        settings = dict(
            template_path=os.path.join(current_dir, 'templates'),
            static_path=os.path.join(current_dir, 'static'),
            cookie_secret='947e5d1dc624bc99421bfc7e8ebad245'
        )

        # Global connection to database
        self.db = scoped_session(sessionmaker(bind=engine))

        super(Application, self).__init__(handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    """The handler for all RequestHandlers to inherit from."""

    @property
    def db(self):
        return self.application.db


if __name__ == "__main__":
    """Start application upon running this file."""
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
