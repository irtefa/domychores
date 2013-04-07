"""A set of test cases for the SignupHandler.

Contents:
    * SignupHandlerTest: A TestCase for the SignupHandler.
"""

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)
import unittest
from handlers.signup import SignupHandler


class SignupHandlerTest(unittest.TestCase):
    """A TestCase containing tests for the """

    def setUp(self):
        """Start up server."""
        pass

    def test_signup(self):
        self.assertTrue(False)

    def runTest(self):
        """Runs all unit tests for this class"""
        unittest.main()

if __name__ == '__main__':
    unittest.main()
