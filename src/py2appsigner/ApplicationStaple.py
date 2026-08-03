
from logging import Logger
from logging import getLogger

from click import secho

from py2appsigner.CommandBasic import CommandBasic
from py2appsigner.environment.Environment import Environment


class ApplicationStaple(CommandBasic):

    def __init__(self, environment: Environment):

        super().__init__(environment=environment)
        self.logger: Logger = getLogger(__name__)

    def execute(self):

        secho('Apple\'s CloudKit Notary Ticket server.', reverse=True)

        stapleIt: str = f'xcrun stapler staple {self._applicationName}'

        self._runCommand(command=stapleIt)
