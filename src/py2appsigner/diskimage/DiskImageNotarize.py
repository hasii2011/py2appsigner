
from logging import Logger
from logging import getLogger

from py2appsigner.CommandBasic import BUILD_DIR
from py2appsigner.CommandBasic import CommandBasic

from py2appsigner.Common import DMG_SUFFIX
from py2appsigner.Common import DEFAULT_NOTARY_TOOL_KEYCHAIN_PROFILE_NAME

from py2appsigner.environment.BasicEnvironment import BasicEnvironment


class DiskImageNotarize(CommandBasic):

    def __init__(self, environment: BasicEnvironment, keyChainProfileName: str = DEFAULT_NOTARY_TOOL_KEYCHAIN_PROFILE_NAME):
        super().__init__(environment=environment)

        self._keyChainProfileName: str    = keyChainProfileName
        self.logger: Logger = getLogger(__name__)

    def execute(self):

        dmgFile:       str = f'{self._fullPath}{BUILD_DIR}{self._basicEnvironment.applicationName}.{DMG_SUFFIX}'

        notarizeIt: str = f'xcrun notarytool submit {dmgFile} --keychain-profile "{self._keyChainProfileName}" --wait'

        self._runCommand(notarizeIt)
