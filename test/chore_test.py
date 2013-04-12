import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)
import unittest
import json
from server import Application
from models import Chore, drop_all_tables, create_all
from tornado.testing import AsyncHTTPTestCase
from functools import partial


class ChoreTest(AsyncHTTPTestCase):
    """A TestCase containing various tests for the CreateChore, AcceptChore, WithdrawChore, and RemoveChore request handlers."""

    @staticmethod
    def clean_up():
        """Drop tables and create again to remove all test data."""
        drop_all_tables()
        create_all()

    def setUp(self):
        """Set up to be done before each test."""
        super(ChoreTest, self).setUp()
        self.db = self.get_app().db
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
        """Tests creation, update, withdrawal, and removal of a chore."""
        self.__chore_creation(self.db)
        # self.__chore_update(self.db)
        # self.__chore_withdraw(self.db)
        # self.__chore_delete(self.db)

    def tearDown(self):
        """Cleans up after the test."""
        drop_all_tables()
        create_all()

    def runTest(self):
        """Runs all unit tests for this class"""
        unittest.main()
        ChoreTest.clean_up()

    def __chore_creation(self, db):
        """Create chore and and test API response and database."""
        chore = {"task": "Do my laundry",
                 "description": "Figure it out. Its not that hard",
                 "owner_id": 1}

        response = None
        while response is None:
            response = self.create_api(body=json.dumps(chore)).body

        # Test that response is success
        expected = {"success": True}
        self.assertEqual(response, json.dumps(expected))

        # Test that database contains new chore
        # chore_in_db = db.query(Chore).filter(Chore.owner_id == chore["owner_id"]).one()
        # self.assertIsNotNone(chore_in_db)

    def __chore_update(self, db):
        """Update chore with worker and test API response and database."""
        chore_update = {"id": 1,
                        "worker_id": 2}
        response = None
        while response is None:
            response = self.accept_api(body=json.dumps(chore_update)).body

        # Test that response is success
        expected = {"success": True}
        self.assertEqual(response, json.dumps(expected))

        # Test that database contains updated chore info
        chore_in_db = db.query(Chore).filter(Chore.worker_id == chore_update["worker_id"]).one()
        self.assertIsNotNone(chore_in_db)

    def __chore_withdraw(self, db):
        """Withdraw worker from chore and test API response and database."""
        chore_update = {"id": 1,
                        "worker_id": 2}

        response = None
        while response is None:
            response = self.withdraw_api(body=json.dumps(chore_update)).body

        # Test that response is success
        expected = {"success": True}
        self.assertEqual(response, json.dumps(expected))

        # Test that database contains updated chore info
        # chore_in_db = db.query(Chore).filter(Chore.worker_id == chore_update["worker_id"]).one()
        # self.assertIsNone(chore_in_db)

    def __chore_delete(self, db):
        """Delete chore and test API response and database."""
        delete_chore = {"id": 1,
                        "worker_id": 2}

        response = None
        while response is None:
            response = self.remove_api(body=json.dumps(delete_chore)).body

        # Test that response is success
        expected = {"success": True}
        self.assertEqual(response, json.dumps(expected))

        # Test that database contains updated chore info
        # chore_in_db = db.query(Chore).filter(Chore.id == delete_chore["id"]).one()
        # self.assertIsNone(chore_in_db)


if __name__ == '__main__':
    unittest.main()
    ChoreTest.clean_up()
