
from unittest import TestSuite
from unittest import main as unitTestMain

from os import environ as osEnviron

from click import ClickException

from py2appsigner.environment.Environment import Environment
from tests.TestBase import TestBase


class TestEnvironment(TestBase):
    """
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testNoIdentity(self):
        try:
            del osEnviron[Environment.IDENTITY]
        except KeyError:
            pass    # May or may not exist;  don't care

        self.assertRaises(ClickException, lambda: self._classConstruction())

    def testCustomIdentity(self):
        """Another test"""
        osEnviron[Environment.IDENTITY] = 'ElGatoMalo'

        env: Environment = self._classConstruction()

        self.assertEqual('ElGatoMalo', env.identity, 'Custom identity failed')

    def _classConstruction(self) -> Environment:
        env: Environment = Environment(pythonVersion='3.10', applicationName='Ozzee', projectDirectory='funky')

        return env


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestEnvironment))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
