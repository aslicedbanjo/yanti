""" Test cases for copy.copy and copy.deepcopy on the namedtuple.
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


import copy

import pytest


@pytest.mark.parametrize(
    "copier",
    (copy.copy, copy.deepcopy,),
    ids=('copy.copy', 'copy.deepcopy',)
)
def test_copy(copier, namedtuple):
    """ Test that copying works.
    """
    NamedTupCopy = namedtuple('NamedTupCopy', 'x y z')  # pylint: disable=invalid-name
    inst = NamedTupCopy(x=10, y=20, z=30)

    copied = copier(inst)
    assert inst == copied
    assert inst._fields == copied._fields
