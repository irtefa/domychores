from base import BaseHandler
from models import Chore
import json


class CreateChoreHandler(BaseHandler):
    """The handler for signing up Users."""

    def post(self):
        # load the chore as a json object
        chore = json.loads(self.request.body)
        # check if we can add the chore
        if self.add_chore(chore):
            self.write({"success": "true"})
        else:
            self.write({"success": "false"})
        self.finish()

    def add_chore(self, chore):
        session = self.db
       # setup sql command to create a chore
        add_chore_info = Chore(chore['task'], chore['description'], chore['owner_id'], chore['worker_id'], chore['posted_at'])
        # add it to the session
        session.add(add_chore_info)
        # commit the query
        try:
            session.commit()
        except:
            session.rollback()
        return True
