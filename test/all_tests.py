"""A script to run all tests for all libraries in the package.
"""

import unittest
from signup_test import SignupHandlerTest


def create_suite():
    """Creates a new TestSuite to run all tests in the module."""
    suite = unittest.TestSuite()
    suite.addTest(SignupHandlerTest())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    suite = create_suite()
    runner.run(suite)
