#!/usr/bin/python3

""" a module to test for the State class """

import unittest

from models.base_model import BaseModel
from models.state import State


class TestState(unittest.TestCase):

    """intialize the test for the State class"""

    def setUp(self):
        """ to test state class """
        self.state = State()

    def test_is_class_attr(self):

        """ test for attribute """
        self.assertTrue(hasattr(self.state, "name"))

    def test_class_attrs(self):

        """ test for calass attribute """

        self.assertIs(type(self.state.name), str)
        self.assertFalse(bool(self.state.name))

    def test_state_is_subclass(self):

        """ test for subclass  """
        self.assertTrue(issubclass(type(self.state), BaseModel))
