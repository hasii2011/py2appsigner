from logging import Logger
from logging import getLogger

from sys import stdout

from subprocess import run as subProcessRun
from subprocess import check_call as subProcessCheckCall

from subprocess import STDOUT

from abc import abstractmethod
from abc import ABC

from click import secho

from py2appsigner.BasicEnvironment import BasicEnvironment

BUILD_DIR:  str = '/dist/'
ZIP_SUFFIX: str = 'zip'

CODE_SIGN_TOOL:            str = '/usr/bin/codesign'
DITTO_TOOL:                str = '/usr/bin/ditto'

COPY_OPTIONS_VERBOSE:          str = '-vp'
COPY_OPTIONS_QUIET:            str = '-p'
REMOVE_OPTIONS_VERBOSE:        str = '-vrf'
REMOVE_OPTIONS_QUIET:          str = '-rf'
CODE_SIGN_OPTIONS_VERBOSE:     str = '-vvvv --force --timestamp --options=runtime'
CODE_SIGN_OPTIONS_QUIET:       str = '--force --timestamp --options=runtime'


class CommandBasic(ABC):

    def __init__(self, environment: BasicEnvironment):

        self._basicEnvironment: BasicEnvironment = environment

        self.baseLogger: Logger = getLogger(__name__)

        self._fullPath:        str = f'{self._basicEnvironment.projectsBase}/{self._basicEnvironment.projectDirectory}'
        self._applicationName: str = f'{self._fullPath}{BUILD_DIR}{self._basicEnvironment.applicationName}.app'

    @abstractmethod
    def execute(self):
        pass

    def _getToolOptions(self, verboseOptions: str, quietOptions: str) -> str:
        if self._basicEnvironment.verbose is True:
            return verboseOptions
        else:
            return quietOptions

    def _runCommand(self,  command: str):

        if self._basicEnvironment.verbose is True:
            secho(self._execute(command=command))
        else:
            subProcessRun([command], shell=True, capture_output=True, text=True, check=True)

    def _execute(self, command):
        subProcessCheckCall(command, shell=True, stdout=stdout, stderr=STDOUT)