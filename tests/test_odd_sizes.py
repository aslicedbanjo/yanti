""" Test cases for namedtuples of odd sizes.
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


def test_empty_eq(empty):
    """ Test empty namedtuple equality with a normal tuple.
    """
    assert empty() == ()


def test_empty_make(empty):
    """ Test _make on empty method.
    """
    assert empty._make([]) == ()


def test_empty_repr(empty):
    """ Assert empty repr is as expected.
    """
    assert repr(empty()) == 'Empty()'


def test_empty_asdict(empty):
    """ Test _asdict on empty namedtuple.
    """
    assert empty()._asdict() == {}


def test_empty_fields(empty):
    """ Test there are no fields on the empty tuple.
    """
    assert empty()._fields == ()


def test_single_equality(single):
    """ Test equality with normal tuple.
    """
    assert single(1) == (1,)


def test_single_make(single):
    """ Test _make method.
    """
    assert single._make([1]) == (1,)


def test_single_attr_access(single):
    """ Test attribute access of single item.
    """
    assert single(1).d == 1


def test_single_repr(single):
    """ Test repr of single item namedtuple.
    """
    assert repr(single(1)) == 'Single(d=1)'


def test_single_asdict(single):
    """ Test _asdict.
    """
    assert single(1)._asdict() == {'d': 1}


def test_single_replace(single):
    """ Test replace factory.
    """
    assert single(1)._replace(d=999) == (999,)


def test_single_fields(single):
    """ Test _fields attibute.
    """
    assert single(1)._fields == ('d',)


def test_large_tuple_equality(big_inst, count):
    """ Test that a namedtuple with many items passes equality
        check with a plain tuple.
    """
    assert big_inst == tuple(range(count))


def test_large_make(big, count):
    """ Test _make works on large number of items.
    """
    assert big._make(range(count)) == tuple(range(count))


def test_large_attributes(big_inst, count, names):
    """ Test that all attributes have the correct values.
    """
    values = [
        getattr(big_inst, name) for name in names
    ]
    assert values == list(range(count))


def test_large_repr(big_inst):
    """ Test that the repr doesn't blow up.
    """
    assert isinstance(repr(big_inst), str)


def test_large_asdict(big_inst, names, count):
    """ Test that _asdict method works as expected.
    """
    dict_ = big_inst._asdict()
    expected = dict(zip(names, range(count)))
    assert dict_ == expected


def test_large_field_names(big_inst, names):
    """ Test that the field names are as expected.
    """
    assert big_inst._fields == tuple(names)


def test_large_replace(big_inst, names, count):
    """ Test _replace method on large instance.
    """
    replacements = {names[1]: 999, names[-5]: 42}
    inst2 = big_inst._replace(**replacements)

    expected = list(range(count))
    expected[1] = 999
    expected[-5] = 42
    assert inst2 == tuple(expected)
