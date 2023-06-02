
from logging import Logger
from logging import getLogger

from py2appsigner.CommandBasic import CommandBasic
from py2appsigner.environment.Environment import Environment


class ApplicationVerify(CommandBasic):

    def __init__(self, environment: Environment):

        super().__init__(environment=environment)

        self.logger: Logger = getLogger(__name__)

    def execute(self):

        verify: str = f'spctl -vvvv --assess --type exec {self._applicationName}'

        self._runCommand(verify)