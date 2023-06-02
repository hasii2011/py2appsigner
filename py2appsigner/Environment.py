
from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from os import environ as osEnvironment

from click import ClickException

from py2appsigner.BasicEnvironment import BasicEnvironment


@dataclass
class Environment(BasicEnvironment):
    """
    """
    IDENTITY:          str = 'IDENTITY'

    DEFAULT_NOTARY_TOOL_APP_ID_NAME: str = 'NOTARY_TOOL_APP_ID'

    pythonVersion:    str = ''
    identity:         str  = ''

    def __init__(self, pythonVersion: str, applicationName: str, projectsBase: str = '', projectDirectory: str = '', identity: str = '', verbose: bool = False):
        """
        Arguments for the command line always override the environment variables

        Args:
            pythonVersion:
            applicationName:
            projectsBase:     Base directory for python projects.
            projectDirectory: The project directory name
            verbose:          'True' if we echo command names and status results from their execution
        """
        super().__init__(applicationName=applicationName, projectsBase=projectsBase, projectDirectory=projectDirectory, verbose=verbose)
        self.logger: Logger = getLogger(__name__)

        self.pythonVersion    = pythonVersion
        self.identity         = identity

        if self.identity == '' or self.identity is None:
            try:
                self.identity = osEnvironment[Environment.IDENTITY]
            except KeyError:
                raise ClickException(message='You must provide the IDENTITY environment variable')
