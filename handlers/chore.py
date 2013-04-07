from base import BaseHandler
from models import Chore
import json


class AcceptChoreHandler(BaseHandler):
    """The handler for accepting a Chore"""

    def post(self):
        # Load the chore as a JSON object
        chore_request = json.loads(self.request.body)
        # Check if we can add the chore
        if self.update_chore(chore_request):
            self.write(json.dumps({"success": True}))
        else:
            self.write(json.dumps({"success": False}))
        self.finish()

    def update_chore(self, chore_request):
        # Check that parameters passed are valid
        if not all(key in chore_request for key in ("id", "worker_id")):
            return False

        session = self.db
        session.query(Chore).filter(Chore.id == chore_request['id']).update({'worker_id': chore_request['worker_id']})
        # Commit the query
        try:
            session.commit()
            return True
        except:
            session.rollback()
            return False


class CreateChoreHandler(BaseHandler):
    """The handler for creating a Chore."""

    def post(self):
        # Load the chore as a JSON object
        chore = json.loads(self.request.body)
        # Check if we can add the chore
        if self.add_chore(chore):
            self.write(json.dumps({"success": True}))
        else:
            self.write(json.dumps({"success": False}))
        self.finish()

    def add_chore(self, chore):
        # Check that parameters passed are valid
        if not all(key in chore for key in ("task", "description", "owner_id", "posted_at")):
            return False

        # Setup SQL command to create a chore
        session = self.db
        add_chore_info = Chore(chore['task'], chore['description'], chore['owner_id'], chore['posted_at'])
        # Add it to the session
        session.add(add_chore_info)
        # Commit the query
        try:
            session.commit()
        except:
            session.rollback()
        return True
