from logging import Logger
from logging import getLogger

from subprocess import run as subProcessRun
from subprocess import CompletedProcess

from abc import abstractmethod
from abc import ABC

from click import secho

from py2appsigner.Environment import Environment

BUILD_DIR:             str = '/dist/'

CODE_SIGN_TOOL:            str = '/usr/bin/codesign'

COPY_OPTIONS_VERBOSE:          str = '-vp'
COPY_OPTIONS_QUIET:            str = '-p'
REMOVE_OPTIONS_VERBOSE:        str = '-vrf'
REMOVE_OPTIONS_QUIET:          str = '-rf'
CODE_SIGN_OPTIONS_VERBOSE:     str = '-vvvv --force --timestamp --options=runtime'
CODE_SIGN_OPTIONS_QUIET:       str = '--force --timestamp --options=runtime'


class CommandBase(ABC):

    def __init__(self, environment: Environment):

        self._environment: Environment = environment

        self.logger: Logger = getLogger(__name__)

        self._fullPath:        str = f'{self._environment.projectsBase}/{self._environment.projectDirectory}'
        self._pythonVersion:   str = self._removeDecimalSeparator(self._environment.pythonVersion)
        self._applicationName: str = f'{self._fullPath}{BUILD_DIR}{self._environment.applicationName}.app'

    @abstractmethod
    def execute(self):
        pass

    def _removeDecimalSeparator(self, pythonVersion: str):
        return pythonVersion.replace('.', '')

    def _getToolOptions(self, verboseOptions: str, quietOptions: str) -> str:
        if self._environment.verbose is True:
            return verboseOptions
        else:
            return quietOptions

    def _runCommand(self,  command: str):

        completedProcess: CompletedProcess = subProcessRun([command], shell=True, capture_output=True, text=True, check=True)
        self._echoCommandAndStatus(command, completedProcess.returncode)

    def _echoCommandAndStatus(self, command: str, status: int):
        if self._environment.verbose is True:
            secho(command)
            secho(f'{status=}')
