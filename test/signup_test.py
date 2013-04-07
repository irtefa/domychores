import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)
import unittest
import json
from server import Application
from models import User
from tornado.testing import AsyncHTTPTestCase
from functools import partial


class SignupTest(AsyncHTTPTestCase):
    """A TestCase containing various tests for the SignupHandler."""

    def setUp(self):
        """Set up to be done before each test."""
        super(SignupTest, self).setUp()
        self.post_request = partial(self.fetch, "/api/signup", method="POST")

    def get_app(self):
        """AsyncHTTPTestCase method to get the application."""
        return Application()

    def test_invalid_signup(self):
        """Tests invalid signup using invalid POST data missing parameters, such as password."""
        post_data = {"first_name": "John", "last_name": "Doe"}
        response = self.post_request(body=json.dumps(post_data)).body

        # Test that response is failure
        expected = {"success": False}
        self.assertEqual(response, json.dumps(expected))

    def test_valid_signup(self):
        """Tests valid signup using valid POST data."""
        post_data = {"first_name": "John",
                     "last_name": "Doe",
                     "email": "john.doe@fail.com",
                     "password": "rishi>=irtefa",
                     "address": "123 Rishi Pwns Irtefa Lane"}
        response = self.post_request(body=json.dumps(post_data)).body

        # Test that response is success
        expected = {"success": True}
        self.assertEqual(response, json.dumps(expected))

        # Test that database contains new user
        db = self.get_app().db
        user = db.query(User).filter(User.email == post_data["email"]).one()
        self.assertIsNotNone(user)

        # Remove inserted user from database
        db.delete(user)
        db.commit()

    def runTest(self):
        """Runs all unit tests for this class"""
        unittest.main()

if __name__ == '__main__':
    unittest.main()
