import os
import tornado.ioloop
import tornado.web
import tornado.httpserver
from handlers.base import MainHandler, LoginHandler
from handlers.user import Login, Logout, Signup, GetUser
from handlers.chore import BrowseChores, GetChore, AcceptChore, CreateChore, RemoveChore, WithdrawChore, CreditOwner, PayWorker
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *


class Application(tornado.web.Application):
    """ The main application class for DoMyChores"""

    PORT = 8888

    def __init__(self):

        handlers = [
            tornado.web.URLSpec(r'/', MainHandler),
            tornado.web.URLSpec(r'/login', LoginHandler),

            # API
            tornado.web.URLSpec(r'/api/signup', Signup),
            tornado.web.URLSpec(r'/api/login', Login),
            tornado.web.URLSpec(r'/api/logout', Logout),

            tornado.web.URLSpec(r'/api/users/([0-9]*)', GetUser),           # GET

            tornado.web.URLSpec(r'/api/chores', BrowseChores),              # GET

            tornado.web.URLSpec(r'/api/chores/([0-9]*)', GetChore),         # GET
            tornado.web.URLSpec(r'/api/chores', CreateChore),               # POST
            tornado.web.URLSpec(r'/api/chores/([0-9]*)', RemoveChore),      # DELETE

            tornado.web.URLSpec(r'/api/chore/([0-9]*)', AcceptChore),      # PUT
            #tornado.web.URLSpec(r'/api/chores/([0-9]*)', WithdrawChore)     # PUT

            tornado.web.URLSpec(r'/api/credit/([0-9]*)', CreditOwner),      # PUT
            tornado.web.URLSpec(r'/api/pay/([0-9]*)', PayWorker),      # PUT
        ]
        current_dir = os.path.dirname(__file__)

        settings = dict(
            login_url="/login",
            static_path=os.path.join(current_dir, 'static'),
            template_path=os.path.join(current_dir, "templates"),
            cookie_secret="33844436e60a85dcafbef8b66efbf1db"
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
