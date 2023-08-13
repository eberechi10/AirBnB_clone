#!/usr/bin/python3

"""a module that defines the Review class."""

from models.base_model import BaseModel


class Review(BaseModel):

    """a method to represent Review."""
    place_id = ""

    user_id: str = ""
    text: str = ""
