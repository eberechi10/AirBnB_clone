#!/usr/bin/python3

"""a module that defines User class."""
from models.base_model import BaseModel


class User(BaseModel):

    """the class to define the User."""
    email: str = ""
    password: str = ""

    first_name: str = ""
    last_name: str = ""
