# coding: utf-8
"""
    brownie.tests.datastructures
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for :mod:`brownie.datastructures`.

    :copyright: 2010-2011 by Daniel Neuhäuser
    :license: BSD, see LICENSE.rst for details
"""
from __future__ import with_statement

from attest import Tests, TestBase, test, Assert

from brownie.datastructures import missing, StackedObject
from brownie.tests.datastructures import (sets, queues, sequences, mappings,
                                          iterators)


class TestMissing(TestBase):
    @test
    def has_false_boolean_value(self):
        if missing:
            raise AssertionError()

    @test
    def repr(self):
        Assert(repr(missing)) == 'missing'

    @test
    def pickleable(self):
        import pickle
        pickled = pickle.dumps(missing)
        unpickled = pickle.loads(pickled)
        if unpickled is not missing:
            raise AssertionError()


class TestStackedObject(TestBase):
    @test
    def top(self):
        s = StackedObject([])
        Assert(s.top) == {}
        s.push({'foo': 'bar'})
        Assert(s.top) == {'foo': 'bar'}
        s.push({'foo': 'baz'})
        Assert(s.top) == {'foo': 'baz'}

    @test
    def stacking(self):
        s = StackedObject([])
        with Assert.raises(AttributeError):
            s.foo

        with Assert.raises(RuntimeError):
            s.pop()

        s.push({'foo': False})
        Assert(s.foo) == False
        s.push({'foo': True})
        Assert(s.foo) == True
        s.pop()
        Assert(s.foo) == False

    @test
    def repr(self):
        s = StackedObject([{}])
        Assert(repr(s)) == 'StackedObject([{}])'


tests = Tests([
    TestMissing, TestStackedObject, queues.tests, sets.tests, sequences.tests,
    mappings.tests, iterators.tests
])
