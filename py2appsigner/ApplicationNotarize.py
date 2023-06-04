
from logging import Logger
from logging import getLogger

from click import clear
from click import secho

from py2appsigner.Common import DEFAULT_NOTARY_TOOL_KEYCHAIN_PROFILE_NAME
from py2appsigner.environment.BasicEnvironment import BasicEnvironment

from py2appsigner.CommandBasic import BUILD_DIR
from py2appsigner.CommandBasic import CommandBasic
from py2appsigner.CommandBasic import DITTO_TOOL
from py2appsigner.CommandBasic import REMOVE_OPTIONS_QUIET
from py2appsigner.CommandBasic import REMOVE_OPTIONS_VERBOSE
from py2appsigner.CommandBasic import ZIP_SUFFIX


class ApplicationNotarize(CommandBasic):

    def __init__(self, environment: BasicEnvironment, keyChainProfileName: str = DEFAULT_NOTARY_TOOL_KEYCHAIN_PROFILE_NAME):
        super().__init__(environment=environment)

        self._keyChainProfileName: str    = keyChainProfileName
        self.logger:               Logger = getLogger(__name__)

    def execute(self):
        #
        #  assumes Xcode 13 is installed
        #  assumes you added an entry APP_PASSWORD to your keychain
        #
        clear()
        zipFile:       str = f'{self._fullPath}{BUILD_DIR}{self._basicEnvironment.applicationName}.{ZIP_SUFFIX}'

        self._cleanupOldZipFile(zipFile=zipFile)
        self._createNewZipFile(zipFile=zipFile)
        self._notarizeIt(zipFile=zipFile)

    def _cleanupOldZipFile(self, zipFile: str):
        # echo "${txReverse}Clean up in case of restart on failure${txReset}"
        # rm - rfv "${ZIP_PATH}"
        # echo    "${txReverse}Clean up in case of restart on failure${txReset}"

        secho('Clean up in case of restart on failure', reverse=True)

        removeOptions: str = self._getToolOptions(verboseOptions=REMOVE_OPTIONS_VERBOSE, quietOptions=REMOVE_OPTIONS_QUIET)
        removeIt:      str = f'rm {removeOptions} {zipFile}'

        self._runCommand(removeIt)

    def _createNewZipFile(self, zipFile: str):
        # echo "${txReverse}Create a ZIP archive suitable for notarization${txReset}"
        # /usr/bin/ditto - c - k - -keepParent "${APP_PATH}" "${ZIP_PATH}"

        secho('Create a ZIP archive suitable for notarization', reverse=True)

        zipIt: str = f'{DITTO_TOOL} -c -k --keepParent {self._applicationName} {zipFile}'

        self._runCommand(zipIt)

    def _notarizeIt(self, zipFile: str):
        secho('Call Apple for notary service', reverse=True)

        # noinspection SpellCheckingInspection
        notarizeIt: str = f'xcrun notarytool submit {zipFile} --keychain-profile "{self._keyChainProfileName}" --wait'

        self._runCommand(notarizeIt)
