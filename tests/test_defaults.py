""" Test cases for defaults parameter.
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


@pytest.fixture
def point_cls_none_defs(namedtuple):
    """ Return a Point namedtuple class with explicit None as defaults
    """
    return namedtuple('Point', 'x y', defaults=None)


@pytest.fixture
def point_cls_no_defaults(namedtuple):
    """ Return a Point namedtuple class with no default values.
    """
    return namedtuple('Point', 'x y', defaults=())


@pytest.fixture
def point_cls_one_default(namedtuple):
    """ Return a Point namedtuple class with one default values.
    """
    return namedtuple('Point', 'x y', defaults=(20,))


# In order to get a new iterator for each instance of this
# fixture, we pass in a "convert" function with a value
# in the request.param. Using iter directly on the value,
# e.g. iter([10, 20]) with result in one instance of the
# fixture having all values from the iterator, and the
# other having none.
@pytest.fixture(
    params=(
        ((10, 20), tuple),
        ((10, 20), list),
        ([10, 20], iter),
    ),
    ids=(
        "tuple-defaults",
        "list-defaults",
        "iter-defaults"
    )
)
def point_cls_two_defaults(request, namedtuple):
    """ Return a Point namedtuple class with two default values.
    """
    val, convert = request.param
    return namedtuple('Point', 'x y', defaults=convert(val))


def test_attr_two_defs(point_cls_two_defaults):  # pylint: disable=redefined-outer-name
    """ Test that the default fields attribute is set correctly.
    """
    # pylint: disable=protected-access
    assert point_cls_two_defaults._fields_defaults == {'x': 10, 'y': 20}


def test_constr_1_two_defs(point_cls_two_defaults):  # pylint: disable=redefined-outer-name
    """ Test that the default fields don't impact construction when all
        parameters are given.
    """
    assert point_cls_two_defaults(1, 2) == (1, 2)


def test_constr_2_two_defs(point_cls_two_defaults):  # pylint: disable=redefined-outer-name
    """ Test that the default fields come into play when one parameter is given.
    """
    assert point_cls_two_defaults(1) == (1, 20)


def test_constr_3_two_defs(point_cls_two_defaults):  # pylint: disable=redefined-outer-name
    """ Test that the default fields come into play when no parameters are given.
    """
    assert point_cls_two_defaults() == (10, 20)


def test_new_attr_two_defs(point_cls_two_defaults):  # pylint: disable=redefined-outer-name
    """ Test that the namedtuple's __new__ has the correct default set.
    """
    assert point_cls_two_defaults.__new__.__defaults__ == (10, 20)


def test_attr_one_def(point_cls_one_default):  # pylint: disable=redefined-outer-name
    """ Test that the default fields attribute is set correctly.
    """
    # pylint: disable=protected-access
    assert point_cls_one_default._fields_defaults == {'y': 20}


def test_constr_1_one_def(point_cls_one_default):  # pylint: disable=redefined-outer-name
    """ Test that the default fields don't impact construction when all
        parameters are given.
    """
    assert point_cls_one_default(1, 2) == (1, 2)


def test_constr_2_one_def(point_cls_one_default):  # pylint: disable=redefined-outer-name
    """ Test that the default fields come into play when one parameter is given.
    """
    assert point_cls_one_default(1) == (1, 20)


def test_attr_no_def(point_cls_no_defaults):  # pylint: disable=redefined-outer-name
    """ Test that the default fields attribute is set correctly.
    """
    # pylint: disable=protected-access
    assert point_cls_no_defaults._fields_defaults == {}


def test_constr_1_no_def(point_cls_no_defaults):  # pylint: disable=redefined-outer-name
    """ Test that the default fields don't impact construction when all
        parameters are given.
    """
    assert point_cls_no_defaults(1, 2) == (1, 2)


def test_constr_err_1_no_def(point_cls_no_defaults):  # pylint: disable=redefined-outer-name
    """ Test that construction fails when only one argument is given
        and no defaults are set.
    """
    with pytest.raises(TypeError):
        point_cls_no_defaults(1)


def test_constr_err_2_no_def(point_cls_no_defaults):  # pylint: disable=redefined-outer-name
    """ Test that construction fails when no arguments are given
        and no defaults are set.
    """
    with pytest.raises(TypeError):
        point_cls_no_defaults()


def test_constr_err_3_no_def(point_cls_no_defaults):  # pylint: disable=redefined-outer-name
    """ Test that construction fails when too many arguments are given
        and no defaults are set.
    """
    with pytest.raises(TypeError):
        point_cls_no_defaults(1, 2, 3)


def test_namedtuple_default_mismatch(namedtuple):
    """ Test that namedtuple type construction when more defaults are given
        than positions.
    """
    with pytest.raises(TypeError):
        namedtuple('Point', 'x y', defaults=(10, 20, 30))


@pytest.mark.parametrize("defaults", (10, False), ids=("int", "bool"))
def test_namedtuple_default_bad_type(namedtuple, defaults):
    """ Test that namedtuple type construction when the given defaults
        are a bad value.
    """
    with pytest.raises(TypeError):
        namedtuple('Point', 'x y', defaults=defaults)


def test_attr_none_def(point_cls_none_defs):  # pylint: disable=redefined-outer-name
    """ Test that the default fields attribute is set correctly.
    """
    # pylint: disable=protected-access
    assert point_cls_none_defs._fields_defaults == {}


def test_new_attr(point_cls_none_defs):  # pylint: disable=redefined-outer-name
    """ Test that the namedtuple's __name__ has the correct default set.
    """
    assert point_cls_none_defs.__new__.__defaults__ is None


def test_constr_1_none_def(point_cls_none_defs):  # pylint: disable=redefined-outer-name
    """ Test that the default fields don't impact construction when all
        parameters are given.
    """
    assert point_cls_none_defs(10, 20) == (10, 20)


def test_constr_err_1_none_def(point_cls_none_defs):  # pylint: disable=redefined-outer-name
    """ Test that construction errors when too few arguments are given.
    """
    with pytest.raises(TypeError):
        point_cls_none_defs(10)
