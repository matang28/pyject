
import unittest

from ioc.core import ResourceContainer, Ioc
from ioc.resources import ResourceKey


class IocComponentsTests(unittest.TestCase):

    def setUp(self):
        ResourceContainer.clear_all()

    def tearDown(self):
        ResourceContainer.clear_all()

    def test_single_component_no_qualifiers(self):

        test1 = ResourceContainer.resolve_resource(ResourceKey(TestClass1))

        self.assertEqual(test1.do(), 1)


@Ioc.component()
class TestClass1(object):
    def __init__(self):
        pass

    def do(self):
        return 1


@Ioc.component()
class TestClass2(object):
    def __init__(self):
        pass

    def do(self):
        return 2


@Ioc.component()
class TestClass3(object):
    def __init__(self, test1: TestClass1, test2: TestClass2):
        self._test1 = test1
        self._test2 = test2

    def do(self):
        return self._test1.do() + self._test2.do()