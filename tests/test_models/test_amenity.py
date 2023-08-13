#!/usr/bin/python3

"""this is test for the amenity class of the models"""

import unittest

from models.base_model import BaseModel
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):

    """ a method to intialize the test for amenity class"""

    def setUp(self):
        self.amenity = Amenity()

    def test_amenity_is_a_subclass(self):
        """ test if amenity is a subclass """
        self.assertTrue(issubclass(type(self.amenity), BaseModel))

    def test_class_attr(self):
        """ if is a class attribute  """
        self.assertTrue(hasattr(self.amenity, "name"))

    def test_class_attr(self):
        self.assertIs(type(self.amenity.name), str)
        self.assertFalse(bool(getattr(self.amenity, "name")))
