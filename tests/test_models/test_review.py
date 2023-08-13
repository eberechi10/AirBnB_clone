#!/usr/bin/python3

"""test for the Review class """

import unittest

from models.base_model import BaseModel
from models.review import Review


class TestReview(unittest.TestCase):
    """method to intialize test for the Review class"""

    def setUp(self):
        """ test for Review class """

        self.review = Review()
        self.attr_list = [
            "place_id",
            "user_id",
            "text"
        ]

    def test_review_is_subclass(self):
        """ test for review is a subclass """

        self.assertTrue(issubclass(type(self.review), BaseModel))

    def test_class_attrs(self):
        """test for type attribute  """

        for attr in self.attr_list:
            self.assertIs(type(getattr(self.review, attr)), str)
            self.assertFalse(bool(getattr(self.review, attr)))

    def test_attrs_are_class_attrs(self):
        """ test for attribute  """

        for attr in self.attr_list:
            self.assertTrue(hasattr(self.review, attr))
