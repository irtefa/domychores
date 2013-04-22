from tornado.web import RequestHandler, authenticated
import json


class BaseHandler(RequestHandler):
    """The handler for all RequestHandlers to inherit from."""

    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user = self.get_secure_cookie("dmc")
        return user


class MainHandler(BaseHandler):
    """The handler to render the JavaScript application."""

    @authenticated
    def get(self):
        user = json.loads(self.get_current_user())
        self.render("index.html", user_id=user["id"])


class LoginHandler(BaseHandler):
    """The handler to render the Login/Signup page."""

    def get(self):
        self.render("signup.html")
