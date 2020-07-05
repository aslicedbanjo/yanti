""" Test cases for the namedtuple factory.
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


import pytest


def test_attribute_name(point_cls):
    """ Test __name__ attribute.
    """
    assert point_cls.__name__ == 'Point'


def test_attribute_slots(point_cls):
    """ Test __slots__ attribute.
    """
    # pylint: disable=no-member
    assert point_cls.__slots__ == ()


def test_attribute_module(point_cls):
    """ Check that the module name on the instance.
    """
    # The __module__ is tests.conftest since that is where
    # the point class namedtuple is defined (tests is a package
    # because it contains a __init__.py file).
    assert point_cls.__module__ == 'tests.conftest'


def test_attribute_getitem_eq(point_cls):
    """ Test inheritance of __getitem__ method.
    """
    # This is equivalent to the original test case testing for
    # inheritence of __getitem__. However, inheritance is
    # stronger - see test_attribute_getitem_identity
    assert point_cls.__getitem__ == tuple.__getitem__


def test_attribute_getitem_identity(point_cls):
    """ Test inheritance of __getitem__ method.
    """
    # Inheritance of methods is stronger, you get the same _object_
    # so the id's match
    assert point_cls.__getitem__ is tuple.__getitem__


def test_attribute_fields(point_cls):
    """ Test that the _fields attributes has the correct fields.
    """
    assert point_cls._fields == ('x', 'y')


def test_constr_fail1(namedtuple):
    """ Check that construction fails when the class name
        has a non-alpha char.
    """
    with pytest.raises(ValueError):
        namedtuple('abc%', 'efg ghi')


def test_constr_fail2(namedtuple):
    """ Check that construction fails when the class name
        is a keyword.
    """
    with pytest.raises(ValueError):
        namedtuple('class', 'efg ghi')


def test_constr_fail3(namedtuple):
    """ Check that construction fails when the class name
        starts with digit.
    """
    with pytest.raises(ValueError):
        namedtuple('9abc', 'efg ghi')


def test_constr_fail4(namedtuple):
    """ Check that construction fails when a field name has
        a non-alpha character.
    """
    with pytest.raises(ValueError):
        namedtuple('abc', 'efg g%hi')


def test_constr_fail5(namedtuple):
    """ Test that construction fails when a field name is a keyword.
    """
    with pytest.raises(ValueError):
        namedtuple('abc', 'abc class')


def test_constr_fail6(namedtuple):
    """ Test that construction fails when a field starts with digit.
    """
    with pytest.raises(ValueError):
        namedtuple('abc', '8efg 9ghi')


def test_constr_fail7(namedtuple):
    """ Test that construction fails when a field has a leading underscore.
    """
    with pytest.raises(ValueError):
        namedtuple('abc', '_efg ghi')


def test_constr_fail8(namedtuple):
    """ Test that construction fails when there is a duplicate field.
    """
    with pytest.raises(ValueError):
        namedtuple('abc', 'efg efg ghi')


def test_construction_1(namedtuple):
    """ Verify that numbers are allowed in attribute names.
    """
    tup = namedtuple('Point0', 'x1 y2')
    assert tup


def test_construction_2(namedtuple):
    """ Test leading underscores in a typename.
    """
    tup = namedtuple('_', 'a b c')
    assert tup


# Test cases for _make method


def test_make(point_cls):
    """ Test instantiation when the correct number of arguments
        is given to _make.
    """
    assert point_cls._make([1, 2])


def test_make_err1(point_cls):
    """ Test _make errors with correct error when too few args
        are given.
    """
    with pytest.raises(TypeError):
        point_cls._make([11])


def test_make_err2(point_cls):
    """ Test _make errors with correct error when too many args
        are given.
    """
    with pytest.raises(TypeError):
        point_cls._make([11, 22, 33])


def test_factory_unicode_1(namedtuple):
    """ Test that leading u is not present in fields repr.
    """
    nt1 = namedtuple('nt', 'the quick brown fox')
    assert "u'" not in repr(nt1._fields)


def test_factory_unicode_2(namedtuple):
    """ Test that unicode is not present in a different namedtuple.
    """
    nt1 = namedtuple('nt', ('the', 'quick'))
    assert "u'" not in repr(nt1._fields)
