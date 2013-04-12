import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)
import unittest
import json
from server import Application
from models import User, Chore
from tornado.testing import AsyncHTTPTestCase
from functools import partial


class ChoreTest(AsyncHTTPTestCase):
    """A TestCase containing various tests for the CreateChore, AcceptChore, WithdrawChore, and RemoveChore request handlers."""

    def setUp(self):
        """Set up to be done before each test."""
        super(ChoreTest, self).setUp()
        self.user_api = partial(self.fetch, "/api/signup", method="POST")

        post_data = {"first_name": "John",
                     "last_name": "Doe",
                     "email": "john.doe@fail.com",
                     "password": "rishi>=irtefa",
                     "address": "123 Rishi Pwns Irtefa Lane"}
        self.user_api(body=json.dumps(post_data))
        post_data = {"first_name": "Jane",
                     "last_name": "Smith",
                     "email": "jsmith@fail.com",
                     "password": "rishi>=irtefa",
                     "address": "321 Rishi Pwns Irtefa Lane"}
        self.user_api(body=json.dumps(post_data))
        post_data = {"first_name": "Bob",
                     "last_name": "Blah",
                     "email": "blah@fail.com",
                     "password": "rishi>=irtefa",
                     "address": "789 Rishi Pwns Irtefa Lane"}
        self.user_api(body=json.dumps(post_data))

        self.create_api = partial(self.fetch, "/api/create_chore", method="POST")
        self.accept_api = partial(self.fetch, "/api/accept_chore", method="POST")
        self.withdraw_api = partial(self.fetch, "/api/remove_chore", method="POST")
        self.remove_api = partial(self.fetch, "/api/withdraw_chore", method="POST")

    def get_app(self):
        """AsyncHTTPTestCase method to get the application."""
        return Application()

    def test_chore_cycle(self):
        """Tests creation, update, windrawal, and removal of a chore."""
        chore = {"task": "Do my laundry",
                 "description": "Figure it out. Its not that hard",
                 "owner_id": 1}
        response = self.create_api(body=json.dumps(chore)).body
        # Test that response is success
        expected = {"success": True}
        self.assertEqual(response, json.dumps(expected))

    def tearDown(self):
        """Tear down users that were created."""
        db = self.get_app().db
        john = db.query(User).filter(User.email == "john.doe@fail.com").one()
        jane = db.query(User).filter(User.email == "jsmith@fail.com").one()
        bob = db.query(User).filter(User.email == "blah@fail.com").one()
        chore = db.query(Chore).filter(Chore.task == "Do my laundry").one()
        # Remove inserted users and chore from database
        db.delete(chore)
        db.commit()
        db.delete(john)
        db.delete(jane)
        db.delete(bob)
        db.commit()

    def runTest(self):
        """Runs all unit tests for this class"""
        unittest.main()

if __name__ == '__main__':
    unittest.main()
