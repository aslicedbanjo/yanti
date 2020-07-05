""" Module providing an alternative implementation of collections.namedtuple.
"""

# Copyright (C) 2019 Dan Jacobs
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import collections
import inspect
import keyword


__all__ = ("namedtuple",)


class Attribute:
    """ Attribute descriptor for namedtuples.

        Named attributes are instance of this class, and store the
        index of the item in the tuple that they match.
    """
    def __init__(self, index):
        """ Initialise the attribute descriptor - index is the index
            into the tuple associated with the item.
        """
        self.__index = index
        self.__doc__ = "Alias for field number {}".format(index)

    def __get__(self, obj, type_=None):
        """ Retrieve the attribute
        """
        if obj is None:
            # Needed when we want to access the descriptor itself
            # e.g. when setting __doc__ manually
            return self
        return obj[self.__index]

    def __set__(self, obj, value):
        """ Set the attribute
        """
        raise AttributeError("Can't set attribute of namedtuple")

    def __delete__(self, obj):
        """ Delete the attribute
        """
        raise AttributeError("Can't delete attribute of namedtuple")


def _check_class_name_valid(name, err_msg_fmt):
    """ Check that a given name is valid for use as a class name.

        Parameters
        ----------
        name: str
            The name to check as being valid as a class name

        err_msg_fmt: str
            A error message with one %s substitution for use in ValueError
            exceptions.

        Raises
        ------
        ValueError in these circumstances:
            - The name is a reserved keyword
            - The name is not a valid Python identifier
    """
    if keyword.iskeyword(name):
        raise ValueError("Name %r is a reserved keyword" % (name,))

    if not name.isidentifier():
        raise ValueError(err_msg_fmt % (name,))


def _check_field_name_valid(field, existing_fields, err_msg_fmt):
    """ Check that a given field is a valid name or not, and isn't
        a duplicate of an earlier field name.

        Parameters
        ----------
        field: str
            The field name to check as being valid as a variable name

        existing_fields: list
            The list of field names found before the given one

        err_msg_fmt: str
            A error message with one %s substitution for use in ValueError
            exceptions.

        Raises
        ------
        ValueError in these circumstances:
            - The field name is a reserved keyword
            - The field name is not a valid Python identifier
            - The field name starts with a leading underscore
            - The field name was already encountered (duplicates are not allowed)
    """
    if keyword.iskeyword(field):
        raise ValueError("Attribute %r is a reserved keyword" % (field,))

    if not field.isidentifier():
        raise ValueError("Attribute %r is not valid as an attribute name" % (field,))

    if field.startswith("_"):
        raise ValueError(err_msg_fmt % (field,))

    if field in existing_fields:
        raise ValueError("Encountered duplicate field name: %s" % (field,))


def _normalise_fields(fields):
    """ Return a tuple of field names from the given string or iterable.

        Parameters
        ----------
        fields: comma-separate str, or iterable of str

        Returns
        -------
        tuple of str: the "raw" field names as given to the namedtuple factory
    """
    if isinstance(fields, str):
        fields = fields.replace(",", " ")
        fields = tuple(attr for attr in fields.split(" ") if attr)

    fields = tuple(str(field) for field in fields)
    return fields


def _calc_module():
    """ Calculate and return the module of the namedtuple from the call stack.

        Parameters
        ----------
        None

        Returns
        -------
        str, if it was possible to determine the current module, else None
    """
    module = None
    stack = inspect.stack()
    if stack:
        # The 2 here corresponds to the depth in the call stack
        # of this function.
        frame = stack[2].frame
        if frame:
            module = frame.f_globals.get("__name__", "__main__")

    return module


def _fix_args(args, kwargs, fields, defaults_dict):
    """ Fix the args tuple and kwargs dict up given the fields list

        Parameters
        ----------
        args: tuple
            The values for the namedtuple passe as positional arguments

        kwargs: dict
            Further values for the namedtuple passed as keyword arguments

        fields: iterable of str
            The field names in order of the namedtuple

        defaults_dict: dict
            The name/default-value dict for the namedtuple

        Returns
        -------
        tuple:
            The resolved values for the namedtuple taking into account any defaults

        Raises
        ------
        TypeError in these circumstances:
            - no defaults are available and the number of args and kwargs doesn't
              total to the number of fields
            - unexpected kwargs are given

    """
    unexpected_kwargs = set(kwargs) - set(fields)
    if unexpected_kwargs:
        msg = "__new__() got unexpected keyword arguments: %s"
        raise TypeError(msg % (unexpected_kwargs,))

    if not defaults_dict:
        # When there are no defaults, all values must be given either
        # as positional or keyword
        if len(args) + len(kwargs) != len(fields):
            missing = set(fields[len(args):]) - set(kwargs)
            msg = "__new__() is missing %d required positional arguments: %s"
            raise TypeError(msg % (len(missing), missing))

    fixed_args = list(args)

    # These are the field names that don't have values from args
    remaining_fields = fields[len(fixed_args):]

    absent_sentinel = object()

    for field in remaining_fields:
        value = kwargs.get(field, absent_sentinel)

        if value is absent_sentinel:
            value = defaults_dict[field]

        fixed_args.append(value)

    return tuple(fixed_args)


def _fix_fields(fields, rename, valid_id_fmt):
    """ Validate the field names, fixing any 'bad' fields if required.

        Parameters
        ----------
        fields: iterable of str
            The field names to validate

        rename: bool
            If True, any invalid field names will have a 'safe' name generated,
            else a ValueError is raised

        valid_id_fmt: str
            A format string for use in exception messages. A single %r
            substitution is expected

        Returns
        -------
        tuple of str
            The fixed field names

        Raises
        ------
        ValueError: if any field name is not valid, and if rename is False.
    """
    fixed_fields = []
    is_bad = False

    for index, field in enumerate(fields):
        is_bad = False
        try:
            _check_field_name_valid(field, fixed_fields, valid_id_fmt)
        except ValueError:
            if not rename:
                raise
            is_bad = True
        finally:
            if is_bad and rename:
                fixed_fields.append("_{}".format(index))
            else:
                fixed_fields.append(field)

    return tuple(fixed_fields)


def _fields_defaults(defaults, fields):
    """ Build the field defaults dictionary for the namedtuple class.

        Parameters
        ----------
        defaults: tuple
            The default values given to the namedtuple

        fields: list of str
            The full list of fields for the namedtuple

        Returns
        -------
        dict: keys are field names and values are the default values

        Raises
        ------
        TypeError if there are more defauls than fields given
    """
    fields_defaults = {}

    if defaults is not None:
        if len(defaults) > len(fields):
            raise TypeError("Got more default values than field names")

        reversed_defaults = reversed(defaults)
        reversed_fields = reversed(fields)
        fields_defaults = dict(zip(reversed_fields, reversed_defaults))

    return fields_defaults


def namedtuple(name, fields, *, rename=False, defaults=None, module=None):
    """ Return a namedtuple with the given attributes
    """
    # The use of the valid_id_fmt message here mimics the behaviour
    # of the standard library implementation - the same error message
    # is used for both invalid class names and invalid field names.
    valid_id_fmt = "Type names and field names must be valid identifiers: %r"

    _check_class_name_valid(name, valid_id_fmt)

    fields = _normalise_fields(fields)

    # Ensure no duplicates in the fields
    if not rename and len(fields) != len(set(fields)):
        raise ValueError("Duplicate fields")

    fields = _fix_fields(fields, rename, valid_id_fmt)

    defaults = tuple(defaults) if defaults else defaults
    fields_defaults = _fields_defaults(defaults, fields)

    class NamedTupleMeta(type):
        """ Metaclass for adding field descriptors on namedtuple classes.
        """
        def __new__(cls, *args, **kwargs):
            obj = super().__new__(cls, *args, **kwargs)

            for (index, name) in enumerate(fields):
                setattr(obj, name, Attribute(index))

            return obj

    class NamedTuple(tuple, metaclass=NamedTupleMeta):
        """ A namedtuple
        """
        _fields = fields
        _fields_defaults = fields_defaults

        # The stdlib namedtuple API allows 'cls' as a field name, so when
        # given as a kwarg, it will throw an error. We use an 'unlikely'
        # name for the first argument of __new__ (just like in the
        # stdlib...).
        def __new__(__cls, *args, **kwargs):  # pylint: disable=bad-classmethod-argument
            fixed_args = _fix_args(
                args, kwargs, __cls._fields, __cls._fields_defaults
            )

            obj = super().__new__(__cls, fixed_args)

            return obj

        # Ditto regarding 'self' as a field name, so we use __self.
        def _replace(__self, **kwargs):  # pylint: disable=no-self-argument
            """ Creating a new namedtuple instance from the current one,
                replacing the given name/values.
            """
            provided_field_names = set(kwargs)
            available_field_names = set(__self._fields)

            if not provided_field_names <= available_field_names:
                unexpected = list(provided_field_names - available_field_names)
                raise ValueError("Got unexpected field names %r" % (unexpected,))

            current = dict(__self._asdict())
            current.update(kwargs)
            return __self.__class__(**current)

        @classmethod
        def _make(cls, iterable):
            """ Create a new instance from the iterable.
            """
            return cls(*iterable)

        def _asdict(self):
            """ Return an instance of collections.OrderedDict mapping
                attribute names to their values.
            """
            return collections.OrderedDict(
                (field_name, self[index])
                for (index, field_name) in enumerate(self._fields)
            )

        def __repr__(self):
            """ Return a repr of the namedtuple.
            """
            vals = ", ".join([
                "{}={}".format(field, getattr(self, field))
                for field in self._fields
            ])
            cls_name = self.__class__.__name__
            return "{}({})".format(cls_name, vals)

        def __getnewargs__(self):
            """ Help with copying and pickling.
            """
            return tuple(self)

    namespace = {
        "__slots__": (),
        "__doc__": "{}({})".format(name, ", ".join(fields))
    }

    if module is not None:
        namespace["__module__"] = module
    else:
        namespace["__module__"] = _calc_module()

    new_type = type(name, (NamedTuple,), namespace)
    new_type.__new__.__defaults__ = defaults
    return new_type
