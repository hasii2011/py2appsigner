
from logging import Logger
from logging import getLogger

from click import secho

from py2appsigner.CommandBasic import CommandBasic
from py2appsigner.environment.Environment import Environment

# noinspection SpellCheckingInspection
SECURITY_ASSESSMENT_COMMAND: str = '/usr/sbin/spctl'


class ApplicationVerify(CommandBasic):

    def __init__(self, environment: Environment):

        super().__init__(environment=environment)

        self.logger: Logger = getLogger(__name__)

    def execute(self):

        secho('Verify signature', reverse=True)
        verify: str = f'{SECURITY_ASSESSMENT_COMMAND} -vvvv --assess --type exec {self._applicationName}'

        self._runCommand(verify)
