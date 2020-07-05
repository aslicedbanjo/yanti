""" Test that name fixing works as expected.
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


@pytest.mark.parametrize(
    "fields, fixed",
    (
        [('efg', 'g%hi'), ('efg', '_1')],  # field with non-alpha char
        [('abc', 'class'), ('abc', '_1')],  # field has keyword
        [('8efg', '9ghi'), ('_0', '_1')],  # field starts with digit
        [('abc', '_efg'), ('abc', '_1')],  # field with leading underscore
        [('abc', 'efg', 'efg', 'ghi'), ('abc', 'efg', '_2', 'ghi')],  # dupe field
        [('abc', '', 'x'), ('abc', '_1', 'x')],  # fieldname is a space
    ),
    ids=(
        'field-with-non-alpha',
        'field-has-keyword',
        'field-starts-with-digit',
        'field-with-leading-underscore',
        'dupe-field',
        'field-name-is-space'
    )
)
def test_name_fixer(fields, fixed, namedtuple):
    """ Test that the field renaming works correctly
    """
    assert namedtuple('NT', fields, rename=True)._fields == fixed
