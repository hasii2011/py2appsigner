from dataclasses import dataclass
from logging import Logger
from logging import getLogger

from os import environ as osEnvironment

from click import ClickException

ENV_PROJECTS_BASE: str = 'PROJECTS_BASE'
ENV_PROJECT:       str = 'PROJECT'
IDENTITY:          str = 'IDENTITY'


@dataclass
class ExternalEnvironment:
    projectsBase:     str = ''
    projectDirectory: str = ''
    identity:         str  = ''

    def __init__(self, projectsBase: str = '', projectDirectory: str = '', identity: str = ''):

        self.logger: Logger = getLogger(__name__)

        self.projectsBase     = projectsBase
        self.projectDirectory = projectDirectory
        self.identity         = identity

        if self.validProjectsBase is False:
            try:
                self.projectsBase = osEnvironment[ENV_PROJECTS_BASE]
            except KeyError:
                raise ClickException(message='I do not know the base directory name of your Python projects')

        if self.validProjectDirectory is False:
            try:
                self.projectDirectory = osEnvironment[ENV_PROJECT]
            except KeyError:
                raise ClickException(message='I do not know the name of the project directory')

        if self.identity == '' or self.identity is None:
            try:
                self.identity = osEnvironment[IDENTITY]
            except KeyError:
                raise ClickException(message='You must provide the IDENTITY environment variable')

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
