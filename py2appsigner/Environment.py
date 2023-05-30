from dataclasses import dataclass
from logging import Logger
from logging import getLogger

from os import environ as osEnvironment

from click import ClickException


@dataclass
class Environment:
    """
    """
    ENV_PROJECTS_BASE: str = 'PROJECTS_BASE'
    ENV_PROJECT:       str = 'PROJECT'
    IDENTITY:          str = 'IDENTITY'

    DEFAULT_NOTARY_TOOL_APP_ID_NAME: str = 'NOTARY_TOOL_APP_ID'

    pythonVersion:    str = ''
    applicationName:  str = ''
    projectsBase:     str = ''
    projectDirectory: str = ''
    verbose:          bool = False
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
        self.logger: Logger = getLogger(__name__)

        self.pythonVersion    = pythonVersion
        self.applicationName  = applicationName
        self.projectsBase     = projectsBase
        self.projectDirectory = projectDirectory
        self.identity         = identity
        self.verbose          = verbose

        if self.projectsBase == '' or self.projectsBase is None:
            try:
                self.projectsBase = osEnvironment[Environment.ENV_PROJECTS_BASE]
            except KeyError:
                raise ClickException(message='I do not know the base directory name of your Python projects')

        if self.projectDirectory == '' or self.projectDirectory is None:
            try:
                self.projectDirectory = osEnvironment[Environment.ENV_PROJECT]
            except KeyError:
                raise ClickException(message='I do not know the name of the project directory')

        if self.identity == '' or self.identity is None:
            try:
                self.identity = osEnvironment[Environment.IDENTITY]
            except KeyError:
                raise ClickException(message='You must provide the IDENTITY environment variable')

    @property
    def validProjectsBase(self) -> bool:
        if self.projectsBase == '' or self.projectsBase is None:
            return False
        else:
            return True

    def validProjectDirectory(self) -> bool:
        if self.projectDirectory == '' or self.projectDirectory is None:
            return False
        else:
            return True

    def __str__(self) -> str:
        return (
            f'pythonVersion=`{self.pythonVersion}` '
            f'applicationName=`{self.applicationName}` '
            f'projectsBase=`{self.projectsBase}` '
            f'projectDirectory=`{self.projectDirectory}`'
        )

    def __repr__(self):
        return self.__str__()
