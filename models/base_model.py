#!/usr/bin/python3

""" a module that defines BaseModel which defines other methods
"""

from models import storage
import uuid
from datetime import datetime


class BaseModel:

    """ it initializes basemodel class."""

    def __init__(self, *args, **kwargs):

        """method thatInitialize the Base instance.
        Args:
            - *args: list arguments
            - **kwargs: dict arguments
        """

        if kwargs is not None and kwargs != {}:
            for key in kwargs:
                if key == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[key] = kwargs[key]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def to_dict(self):

        """ returns dictionary representation of the object."""

        my_dict = self.__dict__.copy()
        my_dict["__class__"] = type(self).__name__
        my_dict["created_at"] = my_dict["created_at"].isoformat()
        my_dict["updated_at"] = my_dict["updated_at"].isoformat()
        return my_dict

    def __str__(self):

        """ a method that returns string representation."""

        return "[{}] ({}) {}".\
            format(type(self).__name__, self.id, self.__dict__)

    def save(self):

        """a method to save and the updated_at attribute
        with current datetime."""

        self.updated_at = datetime.now()
        storage.save()
