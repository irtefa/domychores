import os
import tornado.ioloop
import tornado.web
import tornado.httpserver
from handlers.user import Signup, GetUser
from handlers.chore import BrowseChores, GetChore, AcceptChore, CreateChore, RemoveChore, WithdrawChore
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *


class Application(tornado.web.Application):
    """ The main application class for DoMyChores"""

    PORT = 8888

    def __init__(self):

        handlers = [
            tornado.web.URLSpec(r'/static/(.*)', tornado.web.StaticFileHandler, {"path": "static/index.html"}),
            tornado.web.URLSpec(r'/', tornado.web.RedirectHandler, {"url": "/static/index.html"}),

            # API
            tornado.web.URLSpec(r'/api/users', Signup),
            tornado.web.URLSpec(r'/api/users/([0-9]*)', GetUser),

            tornado.web.URLSpec(r'/api/chores', BrowseChores),
            tornado.web.URLSpec(r'/api/chores/([0-9]*)', GetChore),
            tornado.web.URLSpec(r'/api/chores', CreateChore),
            tornado.web.URLSpec(r'/api/chores/([0-9]*)', RemoveChore),

            tornado.web.URLSpec(r'/api/chores/([0-9]*)', AcceptChore),
            tornado.web.URLSpec(r'/api/chores/([0-9]*)', WithdrawChore)
        ]
        current_dir = os.path.dirname(__file__)

        settings = dict(
            static_path=os.path.join(current_dir, 'static'),
            cookie_secret='947e5d1dc624bc99421bfc7e8ebad245'
        )

        # Global connection to database
        self.db = scoped_session(sessionmaker(bind=engine))

        super(Application, self).__init__(handlers, **settings)

    def start(self):
        """Start the application."""
        server = tornado.httpserver.HTTPServer(Application())
        server.listen(Application.PORT)
        tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    """Start application upon running this file."""
    app = Application()
    app.start()
