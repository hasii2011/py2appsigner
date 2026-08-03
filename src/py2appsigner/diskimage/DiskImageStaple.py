
from logging import Logger
from logging import getLogger

from py2appsigner.CommandBasic import BUILD_DIR
from py2appsigner.CommandBasic import CommandBasic
from py2appsigner.Common import DMG_SUFFIX
from py2appsigner.environment.BasicEnvironment import BasicEnvironment


class DiskImageStaple(CommandBasic):

    def __init__(self, environment: BasicEnvironment):

        super().__init__(environment=environment)
        self.logger: Logger = getLogger(__name__)

    def execute(self):

        dmgFile: str = f'{self._fullPath}{BUILD_DIR}{self._basicEnvironment.applicationName}.{DMG_SUFFIX}'

        baseCmd: str = 'xcrun '
        if self._basicEnvironment.verbose:
            baseCmd = f'{baseCmd} --verbose'

        stapleIt: str = f'{baseCmd} stapler staple {dmgFile}'

        self._runCommand(command=stapleIt)
