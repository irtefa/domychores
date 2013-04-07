from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    """The handler for all RequestHandlers to inherit from."""

    @property
    def db(self):
        return self.application.db

