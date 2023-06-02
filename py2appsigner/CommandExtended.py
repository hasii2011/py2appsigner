
from logging import Logger
from logging import getLogger

from abc import abstractmethod

from py2appsigner.CommandBase import CommandBase
from py2appsigner.Environment import Environment


class CommandExtended(CommandBase):
    def __init__(self, environment: Environment):

        super().__init__(environment=environment)
        self.logger: Logger = getLogger(__name__)

        self._extendedEnvironment: Environment = environment
        self._pythonVersion:       str         = self._removeDecimalSeparator(self._extendedEnvironment.pythonVersion)

    @abstractmethod
    def execute(self):
        pass

    def _removeDecimalSeparator(self, pythonVersion: str):
        return pythonVersion.replace('.', '')
