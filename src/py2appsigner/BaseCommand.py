
from logging import Logger
from logging import getLogger
from subprocess import CalledProcessError

from sys import stdout

from subprocess import run as subProcessRun
from subprocess import check_call as subProcessCheckCall
from subprocess import STDOUT

from click import ClickException
from click import secho


class BaseCommand:
    def __init__(self, verbose: bool = True):

        self._verbose: bool   = verbose
        self.logger:   Logger = getLogger(__name__)

    @property
    def verbose(self) -> bool:
        return self._verbose

    def _getToolOptions(self, verboseOptions: str, quietOptions: str) -> str:

        if self._verbose is True:
            return verboseOptions
        else:
            return quietOptions

    def _runCommand(self,  command: str):

        try:
            if self._verbose is True:
                secho(self._execute(command=command))
            else:
                subProcessRun([command], shell=True, capture_output=True, text=True, check=True)
        except CalledProcessError as cpe:
            raise ClickException(message=f'Fail {cpe.cmd}')

    def _execute(self, command):
        subProcessCheckCall(command, shell=True, stdout=stdout, stderr=STDOUT)
