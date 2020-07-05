""" Test cases for keyword-only args.
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


def test_keyword_only_arguments_1(namedtuple):
    """ Test that rename argument cannot be passed as a
        positional argument.
    """
    # See issue 25628
    with pytest.raises(TypeError):
        # pylint: disable=too-many-function-args
        namedtuple("NT", ["x", "y"], True)


def test_keyword_only_arguments_2(namedtuple):
    """ Test rename kwarg can be passed and renames required fields.
    """
    NT = namedtuple("NT", ["abc", "def"], rename=True)
    assert NT._fields == ("abc", "_1")


def test_keyword_only_arguments_3(namedtuple):
    """ Test rename and verbose arguments cannot be passed
        as positional arguments.
    """
    # pylint: disable=too-many-function-args
    with pytest.raises(TypeError):
        namedtuple("NT", ["abc", "def"], False, True)
