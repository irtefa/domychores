from base import BaseHandler
from models import Chore
import json


class WithdrawChore(BaseHandler):
    """The handler for withdrawing a Chore"""

    def post(self):
        # Load the chore as a JSON object
        withdraw_request = json.loads(self.request.body)
        # Check if we can withdraw from the chore
        if self.withdraw_chore(withdraw_request):
            self.write(json.dumps({"success": True}))
        else:
            self.write(json.dumps({"success": False}))
        self.finish()

    def withdraw_chore(self, withdraw_request):
        # Check that parameters passed are valid
        if not all(key in withdraw_request for key in ("id", "worker_id")):
            return False

        session = self.db
        session.query(Chore).filter(Chore.id == withdraw_request['id']).update({'worker_id': None})
        # Commit the query
        try:
            session.commit()
            return True
        except:
            session.rollback()
            return False


class RemoveChore(BaseHandler):
    """The handler for removing a Chore"""

    def post(self):
        # Load the chore as a JSON object
        remove_request = json.loads(self.request.body)
        # Check if we can remove a chore
        if self.remove_chore(remove_request):
            self.write(json.dumps({"success": True}))
        else:
            self.write(json.dumps({"success": False}))
        self.finish()

    def remove_chore(self, remove_request):
        # Check that parameters passed are valid
        if not all(key in remove_request for key in ("id", "owner_id")):
            return False

        session = self.db
        session.query(Chore).filter(Chore.id == remove_request['id'] and Chore.owner_id == remove_request['owner_id']).delete()
        # Commit the query
        try:
            session.commit()
            return True
        except:
            session.rollback()
            return False


class AcceptChore(BaseHandler):
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


class CreateChore(BaseHandler):
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
