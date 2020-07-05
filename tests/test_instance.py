""" Test cases for instantiation and instances of namedtuples.
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


def test_instantiation_01(point_inst, point_cls):
    """ Test instantiation with all kwargs.
    """
    assert point_inst == point_cls(x=11, y=22)


def test_instantiation_02(point_inst, point_cls):
    """ Test instantiation with one positional argument and
        one kwarg.
    """
    assert point_inst == point_cls(11, y=22)


def test_instantiation_03(point_inst, point_cls):
    """ Test instantiation with kwargs in different order
        to namedtuple definition.
    """
    assert point_inst == point_cls(y=22, x=11)


def test_instantiation_04(point_inst, point_cls):
    """ Test instantiation with tuple unpacking.
    """
    assert point_inst == point_cls(*(11, 22))


def test_instantiation_05(point_inst, point_cls):
    """ Test instantiation with dict unpacking.
    """
    assert point_inst == point_cls(**dict(x=11, y=22))


def test_instantiation_06(point_cls):
    """ Test instantiation with too few args errors.
    """
    with pytest.raises(TypeError):
        point_cls(1)


def test_instantiation_07(point_cls):
    """ Test instantiation with too many args errors.
    """
    with pytest.raises(TypeError):
        point_cls(1, 2, 3)


def test_instantiation_08(point_cls):
    """ Test instantiation with wrong keyword argument errors.
    """
    with pytest.raises(TypeError):
        point_cls(XXX=1, y=2)


def test_instantiation_09(point_cls):
    """ Test instantiation with missing argument errors.
    """
    with pytest.raises(TypeError):
        point_cls(x=1)


def test_instantiation_10(point_inst, point_cls):
    """ Test equality of two instances when instantiating another
        using the _make method.
    """
    assert point_inst == point_cls._make([11, 22])


def test_instantiation_11(point_inst):
    """ Test _fields attribute.
    """
    assert point_inst._fields == ('x', 'y')


def test_instantiation_12(point_inst):
    """ Test equality of two instances when instantiating another
        using the _replace method.
    """
    assert point_inst._replace(x=1) == (1, 22)


def test_instantiation_13(point_inst):
    """ Test _asdict constructs the correct dictionary result.
    """
    assert point_inst._asdict() == dict(x=11, y=22)


def test_instantiation_14(namedtuple):
    """ Verify that the field string can have commas.
    """
    Point = namedtuple('Point', 'x, y')  # pylint: disable=C0103
    inst = Point(x=11, y=22)
    assert repr(inst) == 'Point(x=11, y=22)'


def test_instantiation_15(namedtuple):
    """ Verify that fields spec can be a tuple/non-string instance.
    """
    Point = namedtuple('Point', ('x', 'y'))  # pylint: disable=C0103
    inst = Point(x=11, y=22)
    assert repr(inst) == 'Point(x=11, y=22)'


def test_instantiation_16(point_inst):
    """ Test that an unknown field raises an error.
    """
    with pytest.raises(ValueError):
        point_inst._replace(x=1, error=2)


def test_repr(point_inst):
    """ Test repr is as expected.
    """
    assert repr(point_inst) == 'Point(x=11, y=22)'


def test_no_weakref(point_inst):
    """ Test absense of __weakref__ attribute on namedtuple
        instances.
    """
    assert '__weakref__' not in dir(point_inst)


def test_attribute_access_01(point_inst):
    """ Test first attribute is present.
    """
    x, _ = point_inst  # pylint: disable=C0103
    assert point_inst.x == x


def test_attribute_access_02(point_inst):
    """ Test second attribute is present.
    """
    _, y = point_inst  # pylint: disable=C0103
    assert point_inst.y == y


def test_attribute_access_03(point_inst):
    """ Test that accessing an attribute that doesn't exist errors.
    """
    with pytest.raises(AttributeError):
        getattr(point_inst, 'z')


# Extra tests not present in the Python standard library tests


def test_set_attr_instance(point_inst):
    """ Test that attributes are not writeable.
    """
    with pytest.raises(AttributeError):
        setattr(point_inst, 'x', 33)


def test_del_attr_instance(point_inst):
    """ Test that attributes cannot be removed.
    """
    with pytest.raises(AttributeError):
        delattr(point_inst, 'x')
