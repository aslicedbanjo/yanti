# YANTI - Yet Anther Named Tuple Implementation


## Motivation

At a previous work-place where I worked from 2012 - 2016 we used Python 2.6 and
2.7. The `collections` module in those versions of Python had a
[`namedtuple`](https://docs.python.org/2/library/collections.html#collections.namedtuple)
implementation which I used quite frequently. Being the inquisitive chap I am,
I looked at the source code for it and I found that this used Python's `exec`
statement on a templated string to generate the `namedtuple` class.

Using `exec` isn't great, and in general should be avoided. Aside from
potential security issues (code injection), it can also be expensive, using a
lot of memory. We saw exactly such problems with the one or two places where we
_had_ to use `exec` in our services.

Later in 2016, I changed jobs and started working for a company that used
Python 3.4.  We used [SQLAlchemy](https://www.sqlalchemy.org/) and I spotted
very quickly that SQLAlchemy had its own version of the `namedtuple` called a
[`KeyedTuple`](https://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.util.KeyedTuple).
When I first saw it, I was puzzled as to why they would implement their own
version. After reading around a little I saw that it was due to performance
issues with the standard library's `namedtuple`.

A little while later I started thinking about how you would implement your own
version of `namedtuple`. The first question that came to mind was where to
store the mapping of name to index to attribute. The obvious answer was a
dictionary, but somehow I found that unsatisfactory. A while later a better
answer came to me: descriptors.

So I thought it would make an interesting project learning for myself to
implement my own version of the `namedtuple`. The goals I set myself were:

- no use of `exec`
- must use pure Python
- must pass the same tests that the standard library version passes

I decided to use TDD (test driven development) since `collections.namedtuple`
already had a full test suite in the Python repository, and I felt that would
be a nice approach to see my implementation becoming more and more complete as
I added more code.

I took the test suite for the `namedtuple` from the standard library of Python
3.7.0 and added it to the `yanti` repository in a modified form so that I could
code against that.


## What I learnt

### One assertion per test can be very helpful

Some people disagree with having a single assertion per test method, but when
it comes to TDD, I found that multi-assertion tests makes it harder to get any
sense of progress.

Python's test suite for `collections.namedtuple` follows the multi-assertion
paradigm in each test method. For example, here's an excerpt from the Python
3.7.0 test suite for the built-in `namedtuple`:

```

TestNT = namedtuple('TestNT', 'x y z')    # type used for pickle tests

class TestNamedTuple(unittest.TestCase):

    def test_factory(self):
        Point = namedtuple('Point', 'x y')
        self.assertEqual(Point.__name__, 'Point')
        self.assertEqual(Point.__slots__, ())
        self.assertEqual(Point.__module__, __name__)
        self.assertEqual(Point.__getitem__, tuple.__getitem__)
        self.assertEqual(Point._fields, ('x', 'y'))
        self.assertIn('class Point(tuple)', Point._source)

        self.assertRaises(ValueError, namedtuple, 'abc%', 'efg ghi')       # type has non-alpha char
        self.assertRaises(ValueError, namedtuple, 'class', 'efg ghi')      # type has keyword
        self.assertRaises(ValueError, namedtuple, '9abc', 'efg ghi')       # type starts with digit

        self.assertRaises(ValueError, namedtuple, 'abc', 'efg g%hi')       # field with non-alpha char
        self.assertRaises(ValueError, namedtuple, 'abc', 'abc class')      # field has keyword
        self.assertRaises(ValueError, namedtuple, 'abc', '8efg 9ghi')      # field starts with digit
        self.assertRaises(ValueError, namedtuple, 'abc', '_efg ghi')       # field with leading underscore
        self.assertRaises(ValueError, namedtuple, 'abc', 'efg efg ghi')    # duplicate field

        namedtuple('Point0', 'x1 y2')   # Verify that numbers are allowed in names
        namedtuple('_', 'a b c')        # Test leading underscores in a typename

        nt = namedtuple('nt', 'the quick brown fox')                       # check unicode input
        self.assertNotIn("u'", repr(nt._fields))
        nt = namedtuple('nt', ('the', 'quick'))                           # check unicode input
        self.assertNotIn("u'", repr(nt._fields))

        self.assertRaises(TypeError, Point._make, [11])                     # catch too few args
        self.assertRaises(TypeError, Point._make, [11, 22, 33])             # catch too many args

```

This is a single test method for the `namedtuple` factory function. Notice how
several features of the factory function are tested: various permutations of
valid construction, various permutations of invalid construction, various
attributes of an instance.

While this does a good job from the point of view of coverage, there are
seventeen asserts and hence seventeen separate things that are being tested. If
I'm coding TDD-style, it means I have a long way to go until I get even one
test passing. For this test to pass I'd need to implement:

- correct implementation of factory function
- all error checking for invalid field name
- all expected attributes of a `namedtuple`
- correct implementation of `__repr__`
- correct implementation of `_make`

The other main problem with the multi-assert approach is that the test method
would stop executing at the first failure. This means that even if the
subsequent assertions would have passed, you don't see that. And it can make it
hard to identify exactly how the functionality is broken.

So even though, I started off with this form of the test suite, eventually it
became enough of a hindrance that I decided to rewrite the entire test suite
using a single assert per test.

This helped me to see more easily exactly what I had broken, and, more
crucially, see what was still working, which in turn helped me work out how to
fix the breakages.

While multiple asserts _can_ be useful when testing, I find that they are
better for larger scale tests, such as small integration tests. But even then,
I try to use them sparingly.

### The [`keyword`](https://docs.python.org/3/library/keyword.html) module

I'd not seen this one before, but it was very useful for `yanti`.

The module has a
[`iskeyword()`](https://docs.python.org/3/library/keyword.html#keyword.iskeyword)
function that tests if a given string is a Python keyword or not.

### The [`str.isidentifier()`](https://docs.python.org/3/library/stdtypes.html#str.isidentifier) method

Another useful method, `str.isidentifier` checks if the given string 'is a
valid identifier according to the language definition'. In other words, this
checks if a string can be used as a Python variable or not.

### Python 3.7.0 had re-implemented `collections.namedtuple()`

Part-way through my implementation, I spotted that `collections.namedtuple` had
been reimplemented for Python 3.7.0: they had done away with the big string
template. However `exec()` was still used in a different place (excerpt from
`collections/__init__.py`):

```
    # Create all the named tuple methods to be added to the class namespace

    s = f'def __new__(_cls, {arg_list}): return _tuple_new(_cls, ({arg_list}))'
    namespace = {'_tuple_new': tuple_new, '__name__': f'namedtuple_{typename}'}
    # Note: exec() has the side-effect of interning the field names
    exec(s, namespace)
    __new__ = namespace['__new__']
    __new__.__doc__ = f'Create new instance of {typename}({arg_list})'
    if defaults is not None:
        __new__.__defaults__ = defaults
```

I was about two-thirds of the way through `yanti` when I discovered this, but
decided to continue since I had enjoyed working on it so far.

## Pytest

I've already mentioned that I rewrote the tests from the standard library to
have a single assert per test method. In the process, I also switched to using
[`pytest`](https://docs.pytest.org/en/latest/).

I felt this was useful for the fixtures facility that `pytest` offers, but also
because I could 'simply' use a parametrized fixture to run the test suite
against both `collections.namedtuple` and `yanti.namedtuple`.

## Other miscellaneous notes

- When refactoring the tests, I uncovered a bug in the `yanti` implementation:
  that the named attributes weren't created until the first instance of the
  `namedtuple` had been created. This was hidden by the original standard
  library tests because they had a setup method that created a `namedtuple` and
  on the line beneath created an instance of it.

- I haven't bothered adding a `setup.py` script as I didn't intend `yanti` to
  be packaged or installed.

- To run the tests, create a virtual environment for Python 3.6 or newer.
  Then, install the requirements from `requirements-dev.txt` and then run
  `pytest` - no command line arguments are needed. The `pytest-pythonpath`
  plugin with some config in `setup.cfg` makes importing from the current
  working directory work so that the tests can import `yanti`.

- I had to use a metaclass to create the attributes on the class, which of
  course comes with the usual caveats regarding multiple inheritance. However,
  I don't recall ever subclassing a `namedtuple` and using a metaclass, so this
  would probably be quite rare.

- I have used the GNU GENERAL PUBLIC LICENSE Version 3 for the code. I'm not a
  lawyer, so if this is incorrect please let me know and I'll correct it.
