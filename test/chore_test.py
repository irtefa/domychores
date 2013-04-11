import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)
import unittest
import json
from server import Application
from models import User
from mock import Mock, patch
from tornado.testing import AsyncHTTPTestCase
from functools import partial


class ChoreTest(AsyncHTTPTestCase):
    """A TestCase containing various tests for the CreateChore, AcceptChore, WithdrawChore, and RemoveChore request handlers."""

    def setUp(self):
        """Set up to be done before each test."""
        super(ChoreTest, self).setUp()
        self.create_api = partial(self.fetch, "/api/create_chore", method="POST")
        self.accept_api = partial(self.fetch, "/api/accept_chore", method="POST")
        self.withdraw_api = partial(self.fetch, "/api/remove_chore", method="POST")
        self.remove_api = partial(self.fetch, "/api/withdraw_chore", method="POST")

    def get_app(self):
        """AsyncHTTPTestCase method to get the application."""
        return Application()

    def runTest(self):
        """Runs all unit tests for this class"""
        unittest.main()

if __name__ == '__main__':
    unittest.main()
