
from typing import cast

from logging import Logger
from logging import getLogger

from os import environ as osEnviron

from unittest import TestSuite
from unittest import main as unitTestMain

from click import ClickException

from py2appsigner.BasicEnvironment import BasicEnvironment
from tests.TestBase import TestBase

# import the class you want to test here
# from org.pyut.template import template


class TestBasicEnvironment(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestBasicEnvironment.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestBasicEnvironment.clsLogger

    def tearDown(self):
        pass

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
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestBasicEnvironment))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
