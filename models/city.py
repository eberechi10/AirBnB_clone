#!/usr/bin/python3

"""this module define city class"""

from models.base_model import BaseModel


class City(BaseModel):

    """ amethod that represents city

    """
    state_id: str = ""
    name: str = ""
