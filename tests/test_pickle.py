""" Tests for pickling namedtuples.
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
import pickle

import pytest

import yanti


# We can't used the 'namedtuple' fixture here because the pickle
# test need symbols defined on the module. Instead, we directly
# create the two namedtuples, one from collections and one from yanti.
NamedTupColl = collections.namedtuple(
    'NamedTupColl', 'x y z'
)  # pylint: disable=invalid-name


NamedTupYan = yanti.namedtuple(
    'NamedTupYan', 'x y z'
)  # pylint: disable=invalid-name


@pytest.mark.parametrize(
    "pickle_protocol_version",
    range(-1, pickle.HIGHEST_PROTOCOL + 1),
    ids=tuple(
        'protocol_ver: {}'.format(protocol_ver if protocol_ver > -1 else 'DEFAULT')
        for protocol_ver in range(-1, pickle.HIGHEST_PROTOCOL + 1)
    )
)
@pytest.mark.parametrize(
    "named_tup", (NamedTupColl, NamedTupYan),
    ids=(
        'collections', 'yanti'
    )
)
def test_pickle(pickle_protocol_version, named_tup):
    """ Test pickling with different protocol versions.
    """
    inst = named_tup(x=10, y=20, z=30)
    loads = pickle.loads
    dumps = pickle.dumps

    rehydrated_inst = loads(dumps(inst, pickle_protocol_version))
    assert inst == rehydrated_inst
    assert inst._fields == rehydrated_inst._fields
    assert b'OrderedDict' not in dumps(inst, pickle_protocol_version)
