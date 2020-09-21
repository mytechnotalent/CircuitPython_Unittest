import unittest
from code import foo


class TestCode(unittest.TestCase):
    def test_foo(self):
        """
        test foo functionality
        """
        # Calls
        result = foo('test')

        # Asserts
        self.assertEqual(result, 'test!')
