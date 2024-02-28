import unittest
from code import foo


class TestCode(unittest.TestCase):
    """
    Test class to test code module
    """
    
    def test_foo(self):
        """
        test foo functionality
        """
        # Calls
        result = foo('test')
        
        # Asserts
        self.assertEqual(result, 'test!')

        
if __name__ == '__main__':
    unittest.main()
