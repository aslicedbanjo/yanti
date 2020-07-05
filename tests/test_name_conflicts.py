""" Test that built-in named and keywords can be used in namedtuples.
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


def test_name_conflicts(namedtuple):
    """ Test that names like "self", "cls", "tuple", "itemgetter",
        and "property" can be used as field names.
    """
    NamedTupNameConfl = namedtuple(  # pylint: disable=invalid-name
        'NamedTupNameConfl', 'itemgetter property self cls tuple'
    )
    tup = NamedTupNameConfl(1, 2, 3, 4, 5)
    assert tup == (1, 2, 3, 4, 5)
    newt = tup._replace(itemgetter=10, property=20, self=30, cls=40, tuple=50)
    assert newt == (10, 20, 30, 40, 50)


def test_new_tuple_unpacking(name_conflicts_cls, words):
    """ Test that __new__ handles the interesting words when using
        tuple unpacking.
    """
    values = tuple(range(len(words)))
    instance = name_conflicts_cls(*values)

    assert instance == values


def test_new_dict_unpacking(name_conflicts_cls, words):
    """ Test that __new__ handles the interesting words when using
        dict unpacking.
    """
    values = tuple(range(len(words)))
    instance = name_conflicts_cls(**dict(zip(name_conflicts_cls._fields, values)))

    assert instance == values


def test_make(name_conflicts_cls, words):
    """ Test that _make works correctly with the interesting words.
    """
    values = tuple(range(len(words)))
    instance = name_conflicts_cls._make(values)

    assert instance == values


def test_repr(name_conflicts_inst):
    """ Test that __repr__ works correctly with the interesting words.
    """
    assert repr(name_conflicts_inst)


def test_asdict(name_conflicts_cls, name_conflicts_inst, words):
    """ Test that _asdict works correctly with the interesting words.
    """
    inst = name_conflicts_inst
    values = tuple(range(len(words)))
    assert inst._asdict() == dict(zip(name_conflicts_cls._fields, values))


def test_replace(name_conflicts_cls, name_conflicts_inst, words):
    """ Test that _replace works correctly with the interesting words.
    """
    values = tuple(range(len(words)))
    new_values = tuple(value * 10 for value in values)
    kwargs = dict(zip(name_conflicts_cls._fields, new_values))
    new_instance = name_conflicts_inst._replace(**kwargs)

    assert new_instance == new_values


def test_fields(name_conflicts_cls, words):
    """ Test that _fields has the correct value.
    """
    assert name_conflicts_cls._fields == tuple(words)


def test__getnewargs(name_conflicts_inst, words):
    """ Test that __getnewargs__ has the correct value.
    """
    values = tuple(range(len(words)))
    assert name_conflicts_inst.__getnewargs__() == values
