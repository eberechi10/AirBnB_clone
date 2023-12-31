#!/usr/bin/python3

"""
A module that defines tests for the BaseModel class
"""

import unittest
from time import sleep
import time
import os
from uuid import uuid4
from datetime import datetime, timedelta

import models
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """
    A method to initialize tests for base_model
    """

    def test_BaseModel_instance_has_id(self):
        """Test instance has id as it initializes"""
        b = BaseModel()
        self.assertTrue(hasattr(b, "id"))

    def test_str_representation(self):
        """Test string representation"""
        b = BaseModel()
        self.assertEqual(str(b), "[BaseModel] ({}) {}".format(b.id, b.__dict__))

    def test_ids_is_unique(self):
        """Test ids generated randomly and is uniquely"""
        b1 = BaseModel()
        b2 = BaseModel()
        self.assertNotEqual(b1.id, b2.id)

    def test_type_of_id_is_str(self):
        """Test ids generated as str objects"""
        b = BaseModel()
        self.assertTrue(type(b.id) is str)

    def test_created_at_is_datetime(self):
        """Attribute "created_at" is a datetime object"""
        b = BaseModel()
        self.assertTrue(type(b.created_at) is datetime)

    def test_updated_at_is_datetime(self):
        """Test "updated_at" is a datetime object"""
        b = BaseModel()
        self.assertTrue(type(b.updated_at) is datetime)

    def test_two_models_different_created_at(self):
        """Test "created_at" if two models are different"""
        b1 = BaseModel()
        sleep(0.02)
        b2 = BaseModel()
        sleep(0.02)
        self.assertLess(b1.created_at, b2.created_at)

    def test_args_unused(self):
        """Test "args is not used."""
        b = BaseModel(None)
        self.assertNotIn(None, b.__dict__.values())

    def test_that_created_at_equals_updated_at_initially(self):
        """Test that created_at == updated_at when they are initialized"""
        b = BaseModel()
        created_at_microseconds = int(b.created_at.timestamp() * 1_000_000)
        updated_at_microseconds = int(b.updated_at.timestamp() * 1_000_000)
        time_tolerance_microseconds = 1_000_000
        time_difference = abs(created_at_microseconds - updated_at_microseconds)
        self.assertTrue(time_difference < time_tolerance_microseconds)

    def test_that_save_func_updates_update_at_attr(self):
        """save() updates the updated_at class"""
        b = BaseModel()
        b.save()
        self.assertNotEqual(b.created_at, b.updated_at)
        self.assertGreater(b.updated_at.microsecond, b.created_at.microsecond)

    def test_to_dict_returns_dict(self):
        """BaseModel.to_dict() returns an object dict"""
        b = BaseModel()
        self.assertTrue(type(b.to_dict()) is dict)

    def test_to_dict_returns_class_under(self):
        """Checks if BaseModel.to_dict() has __class__"""
        b = BaseModel()
        self.assertTrue("__class__" in b.to_dict())

    def test_created_at_returned_by_to_dict_iso_string(self):
        """created_at is stored as a str object in ISO format"""
        b = BaseModel()
        self.assertEqual(b.to_dict()["created_at"], b.created_at.isoformat())

    def test_updated_at_returned_by_to_dict_is_iso_string(self):
        """updated_at is stored as a str object in ISO format"""
        b = BaseModel()
        self.assertEqual(b.to_dict()["updated_at"], b.updated_at.isoformat())

    def test_to_dict_returns_accurate_number_of_keys(self):
        """to_dict() returns the expected number of keys and values"""
        b = BaseModel()
        expected = {ky: value for ky, value in b.__dict__.items() if not ky.startswith("_")}
        self.assertEqual(len(b.to_dict()), len(expected) + 1)

    def test_kwargs_passed_is_empty(self):
        """created_at and updated_at are auto-generated if not in kwargs"""
        my_dict = {}
        b = BaseModel(**my_dict)
        self.assertTrue(type(b.id) is str)
        self.assertTrue(type(b.created_at) is datetime)
        self.assertTrue(type(b.updated_at) is datetime)

    def test_when_kwargs_passed_not_empty(self):
        """created_at and updated_at are created from kwargs"""
        my_dict = {
            "id": uuid4(),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        b = BaseModel(**my_dict)
        self.assertEqual(b.id, my_dict["id"])
        self.assertEqual(
            b.created_at, datetime.strptime(my_dict["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
        )
        self.assertEqual(
            b.updated_at, datetime.strptime(my_dict["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
        )

    def test_when_args_and_kwargs_are_passed(self):
        """When args and kwargs are passed, BaseModel ignores args"""
        dat = datetime.now()
        dat_iso = dat.isoformat()
        b = BaseModel("1234", id="234", created_at=dat_iso, name="Moses")
        self.assertEqual(b.id, "234")
        self.assertEqual(b.created_at, dat)
        self.assertEqual(b.name, "Moses")

    def test_when_kwargs_passed_more_than_default(self):
        """BaseModel does not break when kwargs have more than default"""
        my_dict = {
            "id": uuid4(),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "name": "Moses",
        }
        b = BaseModel(**my_dict)
        self.assertTrue(hasattr(b, "name"))

    def test_new_method_not_called_when_dict_passed_to_BaseModel(self):
        """storage.new() not called when BaseModel created from dict"""
        my_dict = {
            "id": uuid4(),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "name": "Firdaus",
        }
        b = BaseModel(**my_dict)
        self.assertTrue(
            b not in models.storage.all().values(),
            "{}".format(models.storage.all().values()),
        )
        del b

        b = BaseModel()
        self.assertTrue(b in models.storage.all().values())

    def test_save_method_updates_updated_at_attr(self):
        """save() method updates 'updated_at' attribute"""
        b = BaseModel()
        sleep(0.02)
        elm = b.updated_at
        b.save()
        self.assertLess(elm, b.updated_at)

    def test_save_can_update_two_or_more_times(self):
        """save method updates 'updated_at' two times"""
        b = BaseModel()
        sleep(0.02)
        elm = b.updated_at
        b.save()
        sleep(0.02)
        node = b.updated_at
        self.assertLess(elm, node)
        sleep(0.01)
        b.save()
        self.assertLess(node, b.updated_at)

    def test_save_update_file(self):
        """file is updated when the 'save' is called"""
        b = BaseModel()
        b.save()
        bd = "BaseModel.{}".format(b.id)
        with open("file.json", encoding="utf-8") as f:
            self.assertIn(bd, f.read())

    def test_to_dict_contains_correct_keys(self):
        """to_dict() returns the expected keys"""
        by_dict = BaseModel().to_dict()
        atts = ("id", "created_at", "updated_at", "__class__")
        for attr in atts:
            self.assertIn(attr, by_dict)

    def test_to_dict_contains_added_attributes(self):
        """new attributes are returned by to_dict()"""
        b = BaseModel()
        atts = ["id", "created_at", "updated_at", "__class__"]
        b.name = "Moses"
        b.email = "Moses@gmail.com"
        atts.extend(["name", "email"])
        for attr in atts:
            self.assertIn(attr, b.to_dict())

    def test_to_dict_output(self):
        """output returned by to_dict()"""
        b = BaseModel()
        dat = datetime.now()
        b.id = "12345"
        b.created_at = b.updated_at = dat
        t_dict = {
            "id": "12345",
            "created_at": dat.isoformat(),
            "updated_at": dat.isoformat(),
            "__class__": "BaseModel",
        }
        self.assertDictEqual(t_dict, b.to_dict())

    def test_to_dict_with_args(self):
        """TypeError returned if argument passed to to_dict()"""
        b = BaseModel()
        with self.assertRaises(TypeError):
            b.to_dict(None)

    def test_to_dict_not_dunder_dict(self):
        """to_dict() is a dict object != to __dict__"""
        bamo = BaseModel()
        self.assertNotEqual(bamo.to_dict(), bamo.__dict__)


if __name__ == "__main__":
    unittest.main()
