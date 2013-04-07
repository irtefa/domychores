import os
import tornado.ioloop
import tornado.web
import tornado.httpserver
from handlers.pages import IndexHandler
from handlers.pages import AboutHandler
from handlers.signup import Signup
from handlers.chore import AcceptChore, CreateChore, RemoveChore, WithdrawChore
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *


class Application(tornado.web.Application):
    """ The main application class for DoMyChores"""

    PORT = 8888

    def __init__(self):

        handlers = [
            tornado.web.URLSpec(r'/', IndexHandler),
            tornado.web.URLSpec(r'/about', AboutHandler),

            # API
            tornado.web.URLSpec(r'/api/signup', Signup),
            tornado.web.URLSpec(r'/api/create_chore', CreateChore),
            tornado.web.URLSpec(r'/api/accept_chore', AcceptChore),
            tornado.web.URLSpec(r'/api/remove_chore', RemoveChore),
            tornado.web.URLSpec(r'/api/withdraw_chore', WithdrawChore)
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

    def start(self):
        """Start the application."""
        server = tornado.httpserver.HTTPServer(Application())
        server.listen(Application.PORT)
        tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    """Start application upon running this file."""
    app = Application()
    app.start()
