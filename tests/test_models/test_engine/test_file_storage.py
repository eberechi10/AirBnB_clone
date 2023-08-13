#!/usr/bin/python3

""" a module to define test for FileStorage in """

import os.path
import unittest

import models
from models import base_model
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.review import Review
from models.place import Place
from models.state import State
from models.amenity import Amenity
from models.city import City


class TestFileStorageInit(unittest.TestCase):
    """ intilizes test for the FileStorage"""

    def file_path_is_private_class_attr(self):
        """test if file_path is private class attribute"""
        self.assertFalse(hasattr(FileStorage(), "__file_path"))

    def objects_is_private_class_attr(self):
        """test if objs is private class attribute"""
        self.assertFalse(hasattr(FileStorage(), "__objects"))

    def init_without_arg(self):
        """test if initialize without the args"""
        self.assertEqual(type(FileStorage()), FileStorage)

    def init_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def storage_initialization(self):
        """if created in __init__.py"""
        self.assertEqual(type(models.storage), FileStorage)


class TestStorageMethods(unittest.TestCase):
    """a module for testing methods present in FileStorage"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass

        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

        FileStorage._FileStorage__objects = {}

    def all_method(self):

        """Tests all() method of FileStorage class"""
        self.assertTrue(type(models.storage.all()) is dict)

        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_reload_method(self):
        my_base = BaseModel()
        my_city = City()
        my_place = Place()
        my_review = Review()
        my_amenity = Amenity()
        my_user = User()
        my_state = State()

        models.storage.save()
        models.storage.reload()
        my_obj = FileStorage._FileStorage__objects

        self.assertIn("BaseModel." + my_base.id, my_obj)
        self.assertIn("Place." + my_place.id, my_obj)
        self.assertIn("City." + my_city.id, my_obj)
        self.assertIn("Amenity." + my_amenity.id, my_obj)
        self.assertIn("Review." + my_review.id, my_obj)
        self.assertIn("User." + my_user.id, my_obj)
        self.assertIn("State." + my_state.id, my_obj)

        with self.assertRaises(TypeError):
            models.storage.reload(None)

    def new_method(self):

        """if the method of the FileStorage class"""
        my_base = BaseModel()
        my_city = City()
        my_place = Place()
        my_review = Review()
        my_amenity = Amenity()
        my_user = User()
        my_state = State()

        self.assertIn("BaseModel." + my_base.id,
                      models.storage.all().keys())
        self.assertIn(my_base, models.storage.all().values())
        self.assertIn("User." + my_user.id, models.storage.all().keys())
        self.assertIn(my_user, models.storage.all().values())
        self.assertIn("Amenity." + my_amenity.id,
                      models.storage.all().keys())
        self.assertIn(my_amenity, models.storage.all().values())
        self.assertIn("Review." + my_review.id,
                      models.storage.all().keys())
        self.assertIn(my_review, models.storage.all().values())
        self.assertIn("State." + my_state.id, models.storage.all().keys())
        self.assertIn(my_state, models.storage.all().values())
        self.assertIn("Place." + my_place.id, models.storage.all().keys())
        self.assertIn(my_place, models.storage.all().values())
        self.assertIn("City." + my_city.id, models.storage.all().keys())
        self.assertIn(my_city, models.storage.all().values())

        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def save_method(self):

        """test save method in FileStorage class"""
        my_base = BaseModel()
        my_user = User()
        my_state = State()
        my_city = City()
        my_place = Place()
        my_review = Review()
        my_amenity = Amenity()

        models.storage.save()

        with open("file.json", "r") as file:
            my_text = file()
            self.assertIn("BaseModel." + my_base.id, my__text)
            self.assertIn("Place." + my_place.id, my__text)
            self.assertIn("City." + my_city.id, my__text)
            self.assertIn("Amenity." + my_amenity.id, my__text)
            self.assertIn("Review." + my_review.id, my__text)
            self.assertIn("User." + my_user.id, my__text)
            self.assertIn("State." + my_state.id, my_text)

        with self.assertRaises(TypeError):
            models.storage.save(None)


if __name__ == "__main__":
    unittest.main()
