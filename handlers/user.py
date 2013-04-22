from base import BaseHandler
from models import User
import json


class Logout(BaseHandler):
    """The handler for logging Users out."""

    def get(self):
        self.clear_cookie("dmc")
        self.redirect("/")


class Login(BaseHandler):
    """The handler for logging Users in."""

    def post(self):
        self.set_header("Content-Type", "application/json")
        user = json.loads(self.request.body)
        existing_user = self.get_existing(user)
        if existing_user is not None:
            self.set_secure_cookie('dmc', json.dumps({"id": existing_user.id, "email": existing_user.email}))
            self.write(json.dumps({"success": True}))
        else:
            self.write(json.dumps({"success": False}))
        self.finish()

    def get_existing(self, user):
        # Check that parameters passed are valid
        if not all(key in user for key in ("email", "password")):
            return None

        # Check if the user alredy exists
        session = self.db
        existing_query = session.query(User).filter(User.email == user['email'])
        count = existing_query.count()

        # If user exists, check for password match
        if count == 1:
            existing_user = existing_query.one()
            if existing_user and existing_user.password == user["password"]:
                return existing_user
        # Return false if user doesn't already exist or password don't match
        return None


class Signup(BaseHandler):
    """The handler for signing up Users."""

    def post(self):
        self.set_header("Content-Type", "application/json")
        user = json.loads(self.request.body)
        if self.add_user(user):
            self.set_secure_cookie('dmc', json.dumps({"email": user["email"]}))
            self.write(json.dumps({"success": True}))
        else:
            self.write(json.dumps({"success": False}))
        self.finish()

    def add_user(self, user):
        # Check that parameters passed are valid
        if not all(key in user for key in ("first_name", "last_name", "email", "password", "address")):
            return False

        # Check if the user alredy exists
        session = self.db
        user_count = session.query(User).filter(User.email == user['email']).count()

       # If user does not exist add the user
        if user_count < 1:
            add_user_info = User(user['first_name'], user['last_name'], user['email'], user['password'], user['address'])
            session.add(add_user_info)
            session.commit()
            return True
        # Return false if user already exists
        else:
            return False


class GetUser(BaseHandler):
    """The handler for getting information for a given User."""

    def get(self, user_id):
        user = self.get_user(user_id)
        self.set_header("Content-Type", "application/json")
        if user is not None:
            user_dict = {"id": user.id,
                         "first_name": user.first_name,
                         "last_name": user.last_name,
                         "email": user.email,
                         "password": user.password,
                         "address": user.address}
            self.write({"success": True, "user": user_dict})
        else:
            self.write(json.dumps({"success": False}))
        self.finish()

    def get_user(self, user_id):
        session = self.db
        user = session.query(User).get(user_id)
        return user
