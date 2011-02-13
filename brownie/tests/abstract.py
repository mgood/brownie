# coding: utf-8
"""
    brownie.tests.abstract
    ~~~~~~~~~~~~~~~~~~~~~~

    Tests for mod:`brownie.abstract`.

    :copyright: 2010-2011 by Daniel Neuhäuser
    :license: BSD, see LICENSE.rst for details
"""
import sys

from attest import Tests, TestBase, test_if, test, Assert

from brownie.itools import product
from brownie.abstract import VirtualSubclassMeta, ABCMeta, AbstractClassMeta


GE_PYTHON_26 = sys.version_info >= (2, 6)


tests = Tests()

@tests.test_if(GE_PYTHON_26)
def test_virtual_subclass_meta():
    from abc import ABCMeta

    class Foo(object):
        __metaclass__ = ABCMeta


    class Bar(object):
        __metaclass__ = ABCMeta


    class Simple(object):
        __metaclass__ = VirtualSubclassMeta
        virtual_superclasses = [Foo, Bar]

    class InheritingSimple(Simple):
        pass

    for a, b in product([Simple, InheritingSimple], [Foo, Bar]):
        Assert.issubclass(a, b)
        Assert.isinstance(a(), b)

    Assert.issubclass(InheritingSimple, Simple)
    Assert.isinstance(InheritingSimple(), Simple)

    class Spam(object):
        __metaclass__ = ABCMeta

    class Eggs(object):
        __metaclass__ = ABCMeta

    class SimpleMonty(object):
        __metaclass__ = VirtualSubclassMeta
        virtual_superclasses = [Spam, Eggs]

    class MultiInheritance(Simple, SimpleMonty):
        pass

    class MultiVirtualInheritance(object):
        __metaclass__ = VirtualSubclassMeta
        virtual_superclasses = [Simple, SimpleMonty]

    for virtual_super_cls in [Foo, Bar, Simple, Spam, Eggs, SimpleMonty]:
        Assert.issubclass(MultiInheritance, virtual_super_cls)
        Assert.isinstance(MultiInheritance(), virtual_super_cls)


class TestABCMeta(TestBase):
    @test_if(GE_PYTHON_26)
    def type_checks_work(self):
        class Foo(object):
            __metaclass__ = ABCMeta

        class Bar(object):
            pass

        Foo.register(Bar)

        Assert.issubclass(Bar, Foo)
        Assert.isinstance(Bar(), Foo)

    @test
    def api_works_cleanly(self):
        class Foo(object):
            __metaclass__ = ABCMeta

        class Bar(object):
            pass

        Foo.register(Bar)

tests.register(TestABCMeta)


@tests.test_if(GE_PYTHON_26)
def test_abstract_class_meta():
    class Foo(object):
        __metaclass__ = ABCMeta

    class Bar(object):
        __metaclass__ = AbstractClassMeta

        virtual_superclasses = [Foo]

    class Baz(object):
        __metaclass__ = VirtualSubclassMeta

        virtual_superclasses = [Bar]

    Assert.issubclass(Baz, Foo)
    Assert.issubclass(Baz, Bar)
