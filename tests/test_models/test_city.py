#!/usr/bin/python3

""" a test for the City class """

import unittest

from models.base_model import BaseModel
from models.city import City


class TestCity(unittest.TestCase):
    """a method to intialize the test fot the City class"""

    def setUp(self):
        """ test the city class """

        self.city = City()
        self.attr_list = ["state_id", "name"]

    def test_attrs_are_class(self):
        """ test if City are attribute """

        for attr in self.attr_list:
            self.assertIs(type(getattr(self.city, attr)), str)
            self.assertFalse(bool(getattr(self.city, attr)))

    def test_city_subclass(self):
        """ if ity is a subclass  """

        self.assertTrue(issubclass(type(self.city), BaseModel))
