
from dataclasses import dataclass
from logging import Logger
from logging import getLogger

from os import environ as osEnvironment

from click import ClickException


@dataclass
class BasicEnvironment:

    ENV_PROJECTS_BASE: str = 'PROJECTS_BASE'
    ENV_PROJECT:       str = 'PROJECT'

    applicationName:  str = ''
    projectsBase:     str = ''
    projectDirectory: str = ''
    verbose:          bool = False

    def __init__(self, applicationName: str = '', projectsBase: str = '', projectDirectory: str = '', verbose: bool = False):
        """
        Arguments for the command line always override the environment variables

        Args:
            applicationName:
            projectsBase:     Base directory for python projects.
            projectDirectory: The project directory name
            verbose:          'True' if we echo command names and status results from their execution
        """
        self.logger: Logger = getLogger(__name__)

        self.applicationName  = applicationName
        self.projectsBase     = projectsBase
        self.projectDirectory = projectDirectory
        self.verbose          = verbose

        if self.validProjectsBase is False:
            try:
                self.projectsBase = osEnvironment[BasicEnvironment.ENV_PROJECTS_BASE]
            except KeyError:
                raise ClickException(message='I do not know the base directory name of your Python projects')

        if self.validProjectDirectory is False:
            try:
                self.projectDirectory = osEnvironment[BasicEnvironment.ENV_PROJECT]
            except KeyError:
                raise ClickException(message='I do not know the name of the project directory')

    @property
    def validProjectsBase(self) -> bool:
        if self.projectsBase == '' or self.projectsBase is None:
            return False
        else:
            return True

    @property
    def validProjectDirectory(self) -> bool:
        if self.projectDirectory == '' or self.projectDirectory is None:
            return False
        else:
            return True
