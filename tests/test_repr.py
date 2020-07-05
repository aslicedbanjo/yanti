""" Test cases for namedtuple repr's.
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


def test_repr_simple(namedtuple):
    """ Test the repr of a simple class
    """
    Class = namedtuple('Class', 'x')  # pylint: disable=invalid-name
    assert repr(Class(1)) == 'Class(x=1)'


def test_repr_simple_subclass(namedtuple):
    """ Test that repr uses the correct class name
    """
    Class = namedtuple('Class', 'x')  # pylint: disable=invalid-name

    class ReprTest(Class):
        """ ReprTest
        """

    assert repr(ReprTest(1)) == 'ReprTest(x=1)'
