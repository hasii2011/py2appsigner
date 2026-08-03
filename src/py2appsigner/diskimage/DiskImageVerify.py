
from logging import Logger
from logging import getLogger

from click import secho

from py2appsigner.CommandBasic import BUILD_DIR
from py2appsigner.CommandBasic import CommandBasic

from py2appsigner.Common import DMG_SUFFIX
from py2appsigner.Common import SECURITY_ASSESSMENT_COMMAND

from py2appsigner.environment.BasicEnvironment import BasicEnvironment


class DiskImageVerify(CommandBasic):

    def __init__(self, environment: BasicEnvironment):

        super().__init__(environment=environment)

        self.logger: Logger = getLogger(__name__)

    def execute(self):

        dmgFile: str = f'{self._fullPath}{BUILD_DIR}{self._basicEnvironment.applicationName}.{DMG_SUFFIX}'

        baseCmd: str = f'{SECURITY_ASSESSMENT_COMMAND} --assess --type install -v'
        if self._basicEnvironment.verbose:
            baseCmd = f'{baseCmd}vvv '

        secho('Verify signature', reverse=True)
        verify: str = f'{baseCmd} {dmgFile}'

        self._runCommand(verify)
