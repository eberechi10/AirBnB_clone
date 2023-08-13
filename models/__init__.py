#!/usr/bin/python3

"""it is __init__ magic method for models"""

from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
