""" conftest for yanti.
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
import string
from random import choice

import pytest

import yanti


@pytest.fixture(
    params=(collections.namedtuple, yanti.namedtuple),
    ids=('collections', 'yanti',)
)
def namedtuple(request):
    """ Parametrized fixture returning the different
        namedtuple implementations.
    """
    return request.param


@pytest.fixture
def point_cls(namedtuple):  # pylint: disable=redefined-outer-name

    """ Return a Point namedtuple class.
    """
    return namedtuple('Point', 'x y')


@pytest.fixture
def point_inst(point_cls):  # pylint: disable=redefined-outer-name
    """ Return an instance of the point class.
    """
    return point_cls(11, 22)


@pytest.fixture
def empty(namedtuple):  # pylint: disable=redefined-outer-name
    """ An empty namedtuple, with no attributes.
    """
    return namedtuple('Empty', '')


@pytest.fixture
def single(namedtuple):  # pylint: disable=redefined-outer-name
    """ A namedtuple, with one attribute.
    """
    return namedtuple('Single', 'd')


@pytest.fixture
def count():
    """ Convenience fixture returning the count of names.
    """
    # Earlier versions of Python raise a SyntaxError when a function
    # has >= 255 arguments. This was changed in Python 3.7.0.
    name_count = 5000
    return name_count


@pytest.fixture
def names(count):  # pylint: disable=redefined-outer-name
    """ Return a list of names for creating namedtuples with many items.
    """
    attr_names = list(set(
        ''.join([choice(string.ascii_letters) for j in range(10)])
        for i in range(count)
    ))
    return attr_names


@pytest.fixture
def big(namedtuple, names):  # pylint: disable=redefined-outer-name
    """ A namedtuple, with many attributes.
    """
    return namedtuple('Big', names)


@pytest.fixture
def big_inst(big, count):  # pylint: disable=redefined-outer-name
    """ An instance of the Big namedtuple with many attributes.
    """
    return big(*range(count))


@pytest.fixture
def words():
    """ Fixture returning a set of words that are "interesting".
    """
    # Broader test of all interesting names taken from the code, old
    # template, and an example
    interesting_words = {
        'Alias', 'At', 'AttributeError', 'Build', 'Bypass', 'Create',
        'Encountered', 'Expected', 'Field', 'For', 'Got', 'Helper',
        'IronPython', 'Jython', 'KeyError', 'Make', 'Modify', 'Note',
        'OrderedDict', 'Point', 'Return', 'Returns', 'Type', 'TypeError',
        'Used', 'Validate', 'ValueError', 'Variables', 'a', 'accessible', 'add',
        'added', 'all', 'also', 'an', 'arg_list', 'args', 'arguments',
        'automatically', 'be', 'build', 'builtins', 'but', 'by', 'cannot',
        'class_namespace', 'classmethod', 'cls', 'collections', 'convert',
        'copy', 'created', 'creation', 'd', 'debugging', 'defined', 'dict',
        'dictionary', 'doc', 'docstring', 'docstrings', 'duplicate', 'effect',
        'either', 'enumerate', 'environments', 'error', 'example', 'exec', 'f',
        'f_globals', 'field', 'field_names', 'fields', 'formatted', 'frame',
        'function', 'functions', 'generate', 'get', 'getter', 'got', 'greater',
        'has', 'help', 'identifiers', 'index', 'indexable', 'instance',
        'instantiate', 'interning', 'introspection', 'isidentifier',
        'isinstance', 'itemgetter', 'iterable', 'join', 'keyword', 'keywords',
        'kwds', 'len', 'like', 'list', 'map', 'maps', 'message', 'metadata',
        'method', 'methods', 'module', 'module_name', 'must', 'name', 'named',
        'namedtuple', 'namedtuple_', 'names', 'namespace', 'needs', 'new',
        'nicely', 'num_fields', 'number', 'object', 'of', 'operator', 'option',
        'p', 'particular', 'pickle', 'pickling', 'plain', 'pop', 'positional',
        'property', 'r', 'regular', 'rename', 'replace', 'replacing', 'repr',
        'repr_fmt', 'representation', 'result', 'reuse_itemgetter', 's', 'seen',
        'self', 'sequence', 'set', 'side', 'specified', 'split', 'start',
        'startswith', 'step', 'str', 'string', 'strings', 'subclass', 'sys',
        'targets', 'than', 'the', 'their', 'this', 'to', 'tuple', 'tuple_new',
        'type', 'typename', 'underscore', 'unexpected', 'unpack', 'up', 'use',
        'used', 'user', 'valid', 'values', 'variable', 'verbose', 'where',
        'which', 'work', 'x', 'y', 'z', 'zip'
    }

    return interesting_words


@pytest.fixture
def name_conflicts_cls(namedtuple, words):  # pylint: disable=redefined-outer-name
    """ A namedtuple class with many names that conflict with built-in and other
        names.
    """
    name_conflict = namedtuple('name_conflict', words)
    return name_conflict


@pytest.fixture
def name_conflicts_inst(name_conflicts_cls, words):  # pylint: disable=redefined-outer-name
    """ A namedtuple instance with many names that conflict with built-in and other
        names.
    """
    values = tuple(range(len(words)))
    instance = name_conflicts_cls(*values)
    return instance
