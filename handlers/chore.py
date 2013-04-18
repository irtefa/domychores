from base import BaseHandler
from models import Chore
import json


class BrowseChores(BaseHandler):
    """The handler for getting all Chores."""

    def get(self):
        self.set_header("Content-Type", "application/json")
        session = self.db
        results = session.query(Chore).all()
        chores = []
        for chore in results:
            chore_dict = {"id": chore.id,
                          "task": chore.task,
                          "description": chore.description,
                          "owner_id": chore.owner_id,
                          "worker_id": chore.worker_id,
                          "posted_at": chore.posted_at}
            chores.append(chore_dict)
        self.write(json.dumps(chores))
        self.finish()


class GetChore(BaseHandler):
    """The handler for getting information for a given Chore."""

    def get(self, chore_id):
        chore = self.get_chore(chore_id)
        self.set_header("Content-Type", "application/json")
        if chore is not None:
            chore_dict = {"id": chore.id,
                          "task": chore.task,
                          "description": chore.description,
                          "owner_id": chore.owner_id,
                          "worker_id": chore.worker_id,
                          "posted_at": chore.posted_at}
            self.write({"success": True, "chore": chore_dict})
        else:
            self.write(json.dumps({"success": False}))
        self.finish()

    def get_chore(self, chore_id):
        session = self.db
        chore = session.query(Chore).get(chore_id)
        return chore


class CreateChore(BaseHandler):
    """The handler for creating a Chore."""

    def post(self):
        self.set_header("Content-Type", "application/json")
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
        if not all(key in chore for key in ("task", "description", "owner_id")):
            return False

        # Setup SQL command to create a chore
        session = self.db
        add_chore_info = Chore(chore['task'], chore['description'], chore['owner_id'])
        # Add it to the session
        session.add(add_chore_info)
        # Commit the query
        try:
            session.commit()
            return True
        except:
            session.rollback()
            return False


class RemoveChore(BaseHandler):
    """The handler for removing a Chore"""

    def post(self, chore_id):
        self.set_header("Content-Type", "application/json")
        # Load the chore as a JSON object
        remove_request = json.loads(self.request.body)
        # Check if we can remove a chore
        if self.remove_chore(chore_id, remove_request):
            self.write(json.dumps({"success": True}))
        else:
            self.write(json.dumps({"success": False}))
        self.finish()

    def remove_chore(self, chore_id, remove_request):
        # Check that parameters passed are valid
        if not all(key in remove_request for key in ("owner_id")):
            return False

        session = self.db
        session.query(Chore).filter(Chore.id == chore_id and Chore.owner_id == remove_request['owner_id']).delete()
        # Commit the query
        try:
            session.commit()
            return True
        except:
            session.rollback()
            return False


class AcceptChore(BaseHandler):
    """The handler for accepting a Chore"""

    def post(self, chore_id):
        self.set_header("Content-Type", "application/json")
        # Load the chore as a JSON object
        chore_request = json.loads(self.request.body)
        # Check if we can add the chore
        if self.update_chore(chore_id, chore_request):
            self.write(json.dumps({"success": True}))
        else:
            self.write(json.dumps({"success": False}))
        self.finish()

    def update_chore(self, chore_id, chore_request):
        # Check that parameters passed are valid
        if not all(key in chore_request for key in ("worker_id")):
            return False

        session = self.db
        session.query(Chore).filter(Chore.id == chore_id).update({'worker_id': chore_request['worker_id']})
        # Commit the query
        try:
            session.commit()
            return True
        except:
            session.rollback()
            return False


class WithdrawChore(BaseHandler):
    """The handler for withdrawing a Chore"""

    def post(self, chore_id):
        self.set_header("Content-Type", "application/json")
        # Load the chore as a JSON object
        withdraw_request = json.loads(self.request.body)
        # Check if we can withdraw from the chore
        if self.withdraw_chore(chore_id, withdraw_request):
            self.write(json.dumps({"success": True}))
        else:
            self.write(json.dumps({"success": False}))
        self.finish()

    def withdraw_chore(self, chore_id, withdraw_request):
        # Check that parameters passed are valid
        if not all(key in withdraw_request for key in ("worker_id")):
            return False

        session = self.db
        session.query(Chore).filter(Chore.id == chore_id).update({'worker_id': None})
        # Commit the query
        try:
            session.commit()
            return True
        except:
            session.rollback()
            return False
