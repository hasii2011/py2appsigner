
from os import environ as osEnviron

from unittest import TestSuite
from unittest import main as unitTestMain

from click import ClickException

from py2appsigner.environment.BasicEnvironment import BasicEnvironment
from tests.TestBase import TestBase


class TestBasicEnvironment(TestBase):
    """
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testNoProjectBase(self):
        try:
            del osEnviron[BasicEnvironment.ENV_PROJECTS_BASE]
        except KeyError:
            pass    # May or may not exist;  don't care

        self.assertRaises(ClickException, lambda: self._classConstruction())

    def testNoProject(self):
        try:
            del osEnviron[BasicEnvironment.ENV_PROJECT]
        except KeyError:
            pass    # May or may not exist;  don't care

        self.assertRaises(ClickException, lambda: self._classConstruction())

    # noinspection PyUnusedLocal
    def _classConstruction(self):
        be: BasicEnvironment = BasicEnvironment()


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestBasicEnvironment))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
