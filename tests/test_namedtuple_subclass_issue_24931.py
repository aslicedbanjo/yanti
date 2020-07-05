""" Test case for namedtuple subclass issue 24931.
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


def test_subclass_issue_24931(namedtuple):
    """ Testing subclass attribute
    """
    class Point(namedtuple('_Point', ['x', 'y'])):
        """ Subclass for testing
        """

    point = Point(3, 4)

    assert point._asdict() == collections.OrderedDict([('x', 3), ('y', 4)])

    point.w = 5  # pylint: disable=W0201,invalid-name
    assert point.__dict__ == {'w': 5}
