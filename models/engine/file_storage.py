#!/usr/bin/python3

"""A module that defines the FileStorage class."""

import json
import datetime
import os


class FileStorage:

    """a method for serializtion and deserialization classes."""

    __file_path = "file.json"
    __objects = {}

    def dict_class(self):
        """a method to return dict of dict_classe and references."""

        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        dict_class = {
                   "BaseModel": BaseModel,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "User": User,
                   "Place": Place,
                   "Review": Review
        }
        return dict_class

    def reload(self):
        """a method to deserializes JSON file to object."""

        if not os.path.exists(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as file:
            dict_obj = json.load(file)
            dict_obj = {k: self.dict_class()[va["__class__"]](**va)
                        for k, va in dict_obj.items()}
            FileStorage.__objects = dict_obj

    def save(self):
        """a method for Serialzes to the JSON file."""

        with open(FileStorage.__file_path, mode="w", encoding="utf-8") as file:
            dan = {k: va.to_dict() for k, va in FileStorage.__objects.items()}
            json.dump(dan, file)

    def all(self):

        """a method to returns __objects dict."""
        return FileStorage.__objects

    def new(self, obj):

        """a method to set new objects in dict."""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def class_attr(self):

        """Returns the valid attributes."""
        class_attr = {
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str},
            "State":
                     {"name": str},
            "City":
                     {"state_id": str,
                      "name": str},
            "Amenity":
                     {"name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
            {"place_id": str,
                         "user_id": str,
                         "text": str}
        }
        return class_attr
