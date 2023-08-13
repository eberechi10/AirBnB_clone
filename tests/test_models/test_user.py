#!/usr/bin/python3

""" a module to test for the User class"""

import unittest
from models.base_model import BaseModel
from models.user import User


class TestUser(unittest.TestCase):
    """a method to intialize test for the User class"""

    def test_user_is_subclass(self):

        """test for subclass """
        idx = User()
        self.assertTrue(issubclass(type(idx), BaseModel))

    def test_attrs_are_class_attrs(self):

        """ intialize the tes for user class """

        idx = User()
        self.assertTrue(hasattr(User, "first_name")
                        and hasattr(User, "last_name"))

    def test_class_attrs(self):

        """ test for class attribute """

        idx = User()
        self.assertIs(type(idx.first_name), str)
        self.assertIs(type(id.last_name), str)
        self.assertTrue(idx.first_name == "")
        self.assertTrue(idx.last_name == "")
