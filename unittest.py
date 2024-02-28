import sys
import traceback


class SkipTest(Exception):
    """
    Class to handle skipping test functionality
    """
    pass


class TestResult:
    """
    Class to handle test result functionality
    """

    def __init__(self):
        self.errorsNum = 0
        self.failuresNum = 0
        self.skippedNum = 0
        self.testsRun = 0

    def wasSuccessful(self):  # noqa
        """
        Method to handle indication of a successful test functionality

        Returns:
            bool
        """
        return self.errorsNum == 0 and self.failuresNum == 0


class AssertRaisesContext:
    """
    Class to handle an assertion raising context
    """

    def __init__(self, exc: Exception):
        """
        Params:
            exc: Exception
        """
        self.expected = exc
        self.raised = None
        self.traceback = None
        self.exception_value = None

    def __enter__(self):
        """
        Magic method to handle enter implementation objects used with the with statement

        Returns:
            object: AssertRaisesContext
        """
        return self

    def __exit__(self, exc_type: type, exc_value: Exception, traceback):
        """
        Magic method to handle exit implementation objects used with the with statement

        Params:
            exc_type: type the raised exception type (class)
            exc_value: Exception the raised exception instance
            traceback: the traceback for the raised exception

        Returns:
            bool
        """
        self.traceback = traceback
        self.raised = exc_type
        self.exception_value = exc_value
        if exc_type is None:
            assert False, '%r not raised' % self.expected
        if issubclass(exc_type, self.expected):
            return True
        # unhandled exceptions will get re-raise: Returning false indicates not handled
        return False


class TestCase:
    """
    Class to handle unittest test case functionality
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup resources and conditions need for the whole suite (TestCase)
        The main test runner executes this one time only before creating an instance of the class
        """
        pass
    @classmethod
    def tearDownClass(cls):
        """
        Release resources and restore conditions after the test suite has finished
        """
        pass
    def setUp(self):
        """
        Setup resources and starting conditions needed for every test in the suite
        The main test runner executes this before calling any test method in the suite
        """
        pass
    def tearDown(self):
        """
        Release resources, and do any needed cleanup after every test in the suite
        The main test runner executes this after calling any test method in the suite
        """
        pass

    def run(self, result: TestResult):
        for name in dir(self):
            if name.startswith('test'):
                print(f'{name} ({self.__qualname__}) ...', end='')  # report progress
                test_method = getattr(self, name)
                self.setUp()  # Pre-test setup (every test)
                try:
                    result.testsRun += 1
                    test_method()
                    print(' ok')
                except SkipTest as e:
                    print(' skipped:', e.args[0])
                    result.skippedNum += 1
                    result.testsRun -= 1  # not run if skipped
                except AssertionError as e:
                    print(' FAIL:', e.args[0] if e.args else 'no assert message')
                    result.failuresNum += 1
                except (SystemExit, KeyboardInterrupt):
                    raise
                except Exception as e: # noqa
                    print(' ERROR', type(e).__name__)
                    print(''.join(traceback.format_exception(e)))
                    result.errorsNum += 1
                finally:
                    self.tearDown()  # Post-test teardown (every test)

    @staticmethod
    def assertAlmostEqual(x, y, places=None, msg='', delta=None):
        """
        Method to handle assert almost equal logic

        Params:
            x: any
            y: any
            places: NoneType, optional
            msg: str, optional
            delta: NoneType, optional
        """
        if x == y:
            return
        if delta is not None and places is not None:
            raise TypeError('specify delta or places not both')
        if delta is not None:
            if abs(x - y) <= delta:
                return
            if not msg:
                msg = '%r != %r within %r delta' % (x, y, delta)
        else:
            if places is None:
                places = 7
            if round(abs(y - x), places) == 0:
                return
            if not msg:
                msg = '%r != %r within %r places' % (x, y, places)
        assert False, msg

    def fail(self, msg=''):  # noqa
        """
        Method to handle fail logic

        Params:
            msg: str, optional
        """
        assert False, msg

    def assertEqual(self, x, y, msg=''):  # noqa
        """
        Method to handle assert equal logic

        Params:
            x: any
            y: any
            msg: str, optional
        """
        if not msg:  # noqa
            msg = '%r vs (expected) %r' % (x, y)
        assert x == y, msg

    def assertNotEqual(self, x, y, msg=''):  # noqa
        """
        Method to handle assert not equal logic

        Params:
            x: any
            y: any
            msg: str, optional
        """
        if not msg:
            msg = '%r not expected to be equal %r' % (x, y)
        assert x != y, msg

    def assertNotAlmostEqual(self, x, y, places=None, msg='', delta=None):  # noqa
        """
        Method to handle assert not almost equal logic

        Params:
            x: any
            y: any
            places: None, optional
            msg: str, optional
            delta: None, optional
        """
        if delta is not None and places is not None:
            raise TypeError("specify delta or places not both")
        if delta is not None:
            if not (x == y) and abs(x - y) > delta:
                return
            if not msg:
                msg = '%r == %r within %r delta' % (x, y, delta)
        else:
            if places is None:
                places = 7
            if not (x == y) and round(abs(y - x), places) != 0:
                return
            if not msg:
                msg = '%r == %r within %r places' % (x, y, places)
        assert False, msg

    def assertIs(self, x, y, msg=''):  # noqa
        """
        Method to handle assert is logic

        Params:
            x: any
            y: any
            msg: str, optional
        """
        if not msg:
            msg = '%r is not %r' % (x, y)
        assert x is y, msg

    def assertIsNot(self, x, y, msg=''):  # noqa
        """
        Method to handle assert is not logic

        Params:
            x: any
            y: any
            msg: str, optional
        """
        if not msg:
            msg = '%r is %r' % (x, y)
        assert x is not y, msg

    def assertIsNone(self, x, msg=''):  # noqa
        """
        Method to handle assert is none logic

        Params:
            x: any
            msg: str, optional
        """
        if not msg:
            msg = '%r is not None' % x
        assert x is None, msg

    def assertIsNotNone(self, x, msg=''):  # noqa
        """
        Method to handle assert is not none logic

        Params:
            x: any
            msg: str, optional
        """
        if not msg:
            msg = '%r is None' % x
        assert x is not None, msg

    def assertTrue(self, x, msg=''):  # noqa
        """
        Method to handle assert true logic

        Params:
            x: any
            msg: str, optional
        """
        if not msg:
            msg = 'Expected %r to be True' % x
        assert x, msg

    def assertFalse(self, x, msg=''):  # noqa
        """
        Method to handle assert false logic

        Params:
            x: any
            msg: str, optional
        """
        if not msg:
            msg = 'Expected %r to be False' % x
        assert not x, msg

    def assertIn(self, x, y, msg=''):  # noqa
        """
        Method to handle assert in logic

        Params:
            x: any
            y: any
            msg: str, optional
        """
        if not msg:
            msg = 'Expected %r to be in %r' % (x, y)
        assert x in y, msg

    def assertNotIn(self, x, y, msg=''):  # noqa
        """
        Method to handle assert not in logic

        Params:
            x: any
            y: any
            msg: str, optional
        """
        if not msg:
            msg = 'Expected %r to not be in %r' % (x, y)
        assert x not in y, msg

    def assertIsInstance(self, x, y, msg=''):  # noqa
        """
        Method to handle assert is instance logic

        Params:
            x: any
            y: any
            msg: str, optional
        """
        assert isinstance(x, y), msg

    @staticmethod
    def assertRaises(exc, func=None, *args, **kwargs):
        """
        Method to handle assert is instance logic

        Params:
            exc: str
            func: NoneType, optional
            *args: any, optional
            **kwargs: any, optional

        Returns:
            object or None
        """
        if func is None:
            return AssertRaisesContext(exc)
        try:
            func(*args, **kwargs)
            assert False, "%r not raised" % exc
        except Exception as e:
            if isinstance(e, exc):
                return None
            raise


def skip(msg):  # noqa
    """
    Function to handle skip logic

    Params:
        msg: str

    Returns:
        object
    """
    def _decor(func):  # noqa
        """
        Inner function to handle private _decor logic

        Params:
            func: function
        Closure:
            msg: str

        Returns:
            object
        """
        def _inner(self):  # noqa
            """
            Inner function to handle replacing original fun with _inner

            Params:
                self: class instance; subclass of TestCase
            Closure:
                msg: str

            Returns:
                object
            """
            raise SkipTest(msg)
        return _inner
    return _decor

def skipIf(cond, msg):  # noqa
    """
    Function to handle skip if logic

    Params:
        cond: str
        msg: str

    Returns:
        object
    """
    if not cond:
        return lambda x: x
    return skip(msg)


def skipUnless(cond, msg):  # noqa
    """
    Function to handle skip unless logic

    Params:
        cond: str
        msg: str

    Returns:
        object
    """
    if cond:
        return lambda x: x
    return skip(msg)


class TestSuite:
    """
    Class to handle unittest test suite functionality
    """

    def __init__(self):
        self.tests = []

    def addTest(self, cls):  # noqa
        """
        Method to handle adding a test functionality

        Params:
            cls: str
        """
        self.tests.append(cls)


class TestRunner:
    """
    Class to handle test runner functionality
    """

    def run(self, suite):  # noqa
        """
        Method to handle test run functionality

        Params:
            suite: TestSuite

        Returns:
            TestResult
        """
        res = TestResult()
        for c in suite.tests:
            run_class(c, res)
        print('Ran %d tests\n' % res.testsRun)
        if res.failuresNum > 0 or res.errorsNum > 0:
            print('FAILED (failures=%d, errors=%d)' % (res.failuresNum, res.errorsNum))
        else:
            msg = 'OK'
            if res.skippedNum > 0:
                msg += ' (%d skipped)' % res.skippedNum
            print(msg)
        return res


def run_class(test_class: TestCase, test_result: TestResult):
    """
    Execute test methods within a test class, handling setup and teardown.

    Params:
        test_class: TestCase subclass indicating the class to run.
        test_result: TestResult instance to update with test outcomes.
    """
    context = 'setUpClass'
    try:
        test_class.setUpClass()
        context = 'instantiate class'
        testing_instance = test_class()
        context = 'run tests'
        testing_instance.run(test_result)
    except Exception as exc:
        print(f'Error in {context} for {test_class.__name__}:')
        traceback_str = traceback.format_exception(exc)
        print(''.join(traceback_str))
        if context != 'run tests':
            context = 'early tearDownClass due to error'

    # Always Proceed with tearDownClass, with varying context
    if context == 'run tests':
        context = 'tearDownClass'
    try:
        test_class.tearDownClass()
    except Exception as exc:
        print(f'Error in {context} for {test_class.__name__}: {exc}')


def main(module='__main__'):
    def test_cases(m):  # noqa
        """
        Function to handle test case running functionality

        Params:
            m: object
        """
        for tn in dir(m):
            c = getattr(m, tn)  # noqa
            if isinstance(c, type) and issubclass(c, TestCase) and c is not TestCase:
                yield c

    m = __import__(module, None, None, ['*'])  # handle tests in folder

    suite = TestSuite()
    for c in test_cases(m):
        suite.addTest(c)

    runner = TestRunner()
    result = runner.run(suite)

    # Terminate with non-zero return code in case of failures
    sys.exit(result.failuresNum > 0)

# cSpell:ignore noqa
