import sys


class SkipTest(Exception):
    """
    Class to handle skipping test functionality
    """
    pass


class AssertRaisesContext:
    """
    Class to handle an assertion raising context
    """

    def __init__(self, exc):
        """
        Params:
            exc: str
        """
        self.expected = exc

    def __enter__(self):
        """
        Magic method to handle enter implementation objects used with the with statement

        Returns:
            str
        """
        return self

    def __exit__(self, exc_type):
        """
        Magic method to handle exit implementation objects used with the with statement

        Params:
            exc_type: str

        Returns:
            bool
        """
        if exc_type is None:
            assert False, '%r not raised' % self.expected
        if issubclass(exc_type, self.expected):
            return True
        return False


class TestCase:
    """
    Class to handle unittest test case functionality
    """

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
                return
            raise


def skip(msg):  # noqa
    """
    Function to handle skip logic

    Params:
        msg: str

    Returns:
        object
    """
    def _decor(msg):  # noqa
        """
        Inner function to handle private _decor logic

        Params:
            msg: str

        Returns:
            object
        """
        def _inner(self):  # noqa
            """
            Inner function to handle replacing original fun with _inner

            Params:
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
            suite: object

        Returns:
            object
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


def run_class(c, test_result):
    """
    Function to handle running of class functionality

    Params:
        c: object
        test_result: bool
    """
    o = c()
    set_up = getattr(o, 'setUp', lambda: None)
    tear_down = getattr(o, 'tearDown', lambda: None)
    for name in dir(o):
        if name.startswith('test'):
            print('%s (%s) ...' % (name, c.__qualname__), end='')
            m = getattr(o, name)
            set_up()
            try:
                test_result.testsRun += 1
                m()
                print(' ok')
            except SkipTest as e:
                print(' skipped:', e.args[0])
                test_result.skippedNum += 1
            except:  # noqa
                print(' FAIL')
                test_result.failuresNum += 1
                raise
            finally:
                tear_down()


def main(module='__main__'):
    def test_cases(m):  # noqa
        """
        Function to handle test case running functionality

        Params:
            m: object
        """
        for tn in dir(m):
            c = getattr(m, tn)  # noqa
            if isinstance(c, object) and isinstance(c, type) and issubclass(c, TestCase):
                yield c

    m = __import__(module)

    suite = TestSuite()
    for c in test_cases(m):
        suite.addTest(c)

    runner = TestRunner()
    result = runner.run(suite)

    # Terminate with non-zero return code in case of failures
    sys.exit(result.failuresNum > 0)
