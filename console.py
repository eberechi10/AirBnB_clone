#!/usr/bin/python3

import cmd
import re
from shlex import split
from models.base_model import BaseModel
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.user import User
from models.state import State
from models.city import City
from models import storage


class HBNBCommand(cmd.Cmd):

    """A module to the HBNB CMD interpreter."""

    prompt = "(hbnb) "
    """ dict that have the classes to be created """

    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Place": Place,
        "Amenity": Amenity,
        "Review": Review
    }

    def my_check(self, arg):

        """A method to check arguments."""

        curly = re.search(r"\{(.*?)\}", arg)
        bckets = re.search(r"\[(.*?)\]", arg)

        if curly is None:
            if bckets is None:
                return [idx.strip(",") for idx in split(arg)]
            else:
                lex = split(arg[:bckets.span()[0]])
                rel = [idx.strip(",") for idx in lex]
                rel.append(bckets.group())
                return rel
        else:
            lex = split(arg[:curly.span()[0]])
            rel = [idx.strip(",") for idx in lex]
            rel.append(curly.group())
            return rel

    def emptyline(self):
        """Do nothing if the line is an empty line."""
        pass

    def default(self, arg):
        """A method to handle default arg."""
        arg_dict = {
            "all": self.do_all,
            "count": self.do_count,
            "update": self.do_update,
            "show": self.do_show,
            "destroy": self.do_destroy
        }

        node = re.search(r"\.", arg)
        if node is not None:
            ng_arg = [arg[:node.span()[0]], arg[node.span()[1]:]]
            node = re.search(r"\((.*?)\)", ng_arg[1])

            if node is not None:
                my_comd = [ng_arg[1][:node.span()[0]], node.group()[1:-1]]
                if my_comd[0] in arg_dict.keys():
                    call = "{} {}".format(ng_arg[0], my_comd[1])
                    return arg_dict[my_comd[0]](call)
        print("Invalid syntax: {}".format(arg))
        return False

    def do_quit(self, arg):

        """A method to exit the program."""
        return True

    def do_EOF(self, arg):

        """A method to signal the exit from the program."""
        print("")
        return True

    def do_create(self, arg):
        """ A method to create a new class instance of BaseModel. """
        ng_arg = self.my_check(arg)
        if len(ng_arg) == 0:
            print("** class name missing **")
        elif ng_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            new_instance = HBNBCommand.__classes[ng_arg[0]]()
            print(new_instance.id)
            storage.save()

    def do_count(self, arg):
        """A method to count the number of instances in the class."""
        ng_arg = self.my_check(arg)
        total = 0

        for obj in storage.all().values():
            if ng_arg[0] == obj.__class__.__name__:
                total += 1
        print(total)

    def do_update(self, arg):
        """A method to update class instance based on class name and id"""
        ng_arg = self.my_check(arg)
        obj_dict = storage.all()

        if len(ng_arg) == 0:
            print("** class name missing **")
            return False
        if ng_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False

        if len(ng_arg) == 1:
            print("** instance id missing **")
            return False

        if "{}.{}".format(ng_arg[0], ng_arg[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(ng_arg) == 2:
            print("** attribute name missing **")
            return False

        if len(ng_arg) == 3:
            if not ng_arg[2].startswith("{"):
                print("** value missing **")
                return False

        if len(ng_arg) == 4:
            obj = obj_dict["{}.{}".format(ng_arg[0], ng_arg[1])]
            if ng_arg[2] in obj.__class__.__dict__.keys():
                v_type = type(obj.__class__.__dict__[ng_arg[2]])
                obj.__dict__[ng_arg[2]] = v_type(ng_arg[3])
            else:
                obj.__dict__[ng_arg[2]] = ng_arg[3]
        elif ng_arg[2].startswith("{"):
            obj = obj_dict["{}.{}".format(ng_arg[0], ng_arg[1])]
            for k, i in eval(ng_arg[2]).items():

                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    v_type = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = v_type(i)
                else:
                    obj.__dict__[k] = i
        storage.save()

    def do_show(self, arg):

        """A method to display the string representation of an instance."""
        ng_arg = self.my_check(arg)
        obj_dict = storage.all()

        if len(ng_arg) == 0:
            print("** class name missing **")
        elif ng_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(ng_arg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(ng_arg[0], ng_arg[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(ng_arg[0], ng_arg[1])])

    def do_destroy(self, arg):

        """A method to delete a class instance by class name and id."""
        ng_arg = self.my_check(arg)
        obj_dict = storage.all()
        if len(ng_arg) == 0:
            print("** class name missing **")
        elif ng_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(ng_arg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(ng_arg[0], ng_arg[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(ng_arg[0], ng_arg[1])]
            storage.save()

    def do_all(self, arg):

        """A method to display string representations of all instances."""
        ng_arg = self.my_check(arg)
        if len(ng_arg) > 0 and ng_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            obj_list = []
            for obj in storage.all().values():
                if len(ng_arg) > 0 and ng_arg[0] == obj.__class__.__name__:
                    obj_list.append(obj.__str__())
                elif len(ng_arg) == 0:
                    obj_list.append(obj.__str__())
            print(obj_list)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
