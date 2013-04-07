from base import BaseHandler
from models import User
import simplejson as json


class SignupHandler(BaseHandler):
    """The handler for signing up Users."""

    def post(self):
        user = json.loads(self.request.body)
        if self.add_user(user):
            self.write({"success": "true"})
        else:
            self.write({"success": "false"})
        self.finish()

    def add_user(self, user):
        session = self.db
        # check if the user alredy exists
        user_count = session.query(User).filter(User.email == user['email']).count()
       # if user does not exist add the user
        if user_count < 1:
            add_user_info = User(user['first_name'], user['last_name'], user['email'], user['password'], user['address'])
            session.add(add_user_info)
            session.commit()
            return True
        # return false if user already exists
        else:
            return False
