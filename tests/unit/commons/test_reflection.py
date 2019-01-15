
import unittest

from commons.reflection import get_constructor_arguments


class ReflectionConstructorTests(unittest.TestCase):

    def test_get_constructor_empty(self):

        # Act:
        args = get_constructor_arguments(TestClass1)

        # Assert:
        self.assertEqual(len(args), 0)

    def test_get_constructor_no_type(self):

        # Act:
        args = get_constructor_arguments(TestClass2)

        # Assert:
        self.assertEqual(len(args), 1)
        self.assertTrue(args["value"] is not None)

    def test_get_constructor_has_type(self):

        # Act:
        args = get_constructor_arguments(TestClass3)

        # Assert:
        self.assertEqual(len(args), 2)
        self.assertTrue(issubclass(TestClass1, args["cls1"]))
        self.assertTrue(issubclass(TestClass2, args["cls2"]))


class TestClass1(object):
    def __init__(self):
        pass

    def get_something(self):
        return "something1"


class TestClass2(object):
    def __init__(self, value):
        self._value = value

    def get_something(self):
        return "something2"


class TestClass3(object):
    def __init__(self, cls1: TestClass1, cls2: TestClass2):
        self._cls1 = cls1
        self._cls2 = cls2

    def get_something_from_one(self):
        return self._cls1.get_something()

    def get_something_from_two(self):
        return self._cls2.get_something()
