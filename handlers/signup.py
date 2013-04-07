from base import BaseHandler
from models import User
import json


class SignupHandler(BaseHandler):
    """The handler for signing up Users."""

    def post(self):
        user = json.loads(self.request.body)
        if self.add_user(user):
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
