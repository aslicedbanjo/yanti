""" Test that the namedtuple behaves like a tuple.
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


def test_tupleness_01(point_inst):
    """ Test that a namedtuple is an instance of a tuple.
    """
    assert isinstance(point_inst, tuple)


def test_tupleness_02(point_inst):
    """ Test tuple equality with a normal tuple.
    """
    assert point_inst == (11, 22)


def test_tupleness_03(point_inst):
    """ Test that a namedtuple can be coerced into a tuple.
    """
    assert tuple(point_inst) == (11, 22)


def test_tupleness_04(point_inst):
    """ Test that a namedtuple can be coerced into a list.
    """
    assert list(point_inst) == [11, 22]


def test_tupleness_05(point_inst):
    """ Test iterable with max function.
    """
    assert max(point_inst) == 22


def test_tupleness_06(point_inst):
    """ Test star-able.
    """
    assert max(*point_inst) == 22


def test_tupleness_07(point_inst):
    """ Test namedtuple unpacks like a tuple.
    """
    x, y = point_inst  # pylint: disable=C0103
    assert point_inst == (x, y)


def test_tupleness_08(point_inst):
    """ Test namedtuple's are indexable like a tuple.
    """
    assert (point_inst[0], point_inst[1]) == (11, 22)


def test_tupleness_09(point_inst):
    """ Test no third item.
    """
    with pytest.raises(IndexError):
        point_inst.__getitem__(3)
