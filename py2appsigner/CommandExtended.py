
from logging import Logger
from logging import getLogger

from abc import abstractmethod

from py2appsigner.CommandBasic import CommandBasic
from py2appsigner.environment.Environment import Environment


class CommandExtended(CommandBasic):
    def __init__(self, environment: Environment):

        super().__init__(environment=environment)
        self.logger: Logger = getLogger(__name__)

        self._extendedEnvironment: Environment = environment
        self._pythonVersion:       str         = self._extendedEnvironment.pythonVersion
        self._flatPythonVersion:   str         = self._removeDecimalSeparator(self._extendedEnvironment.pythonVersion)

    @abstractmethod
    def execute(self):
        pass

    def _removeDecimalSeparator(self, pythonVersion: str):
        return pythonVersion.replace('.', '')
